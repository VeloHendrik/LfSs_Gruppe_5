import math
import random
import time
from agents.hex_state import HexState, evaluate_state

class Node:
    def __init__(self, state, move=None, parent=None):
        self.state = state        # Instanz von HexState
        self.move = move          # Der Zug, der zu diesem Zustand geführt hat
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_possible_moves())

    def best_child(self, c_param=1.0, player=None):
        """
        Wählt das Kind mit dem höchsten UCB1-Wert plus einem progressive bias,
        der aus der statischen Bewertung abgeleitet wird.
        """
        choices = []
        for child in self.children:
            if child.visits == 0:
                ucb = float('inf')
            else:
                ucb = (child.wins / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            bias = 0.0005 * evaluate_state(child.state, player)
            choices.append((ucb + bias, child))
        return max(choices, key=lambda x: x[0])[1]

    def expand(self):
        possible_moves = self.state.get_possible_moves()
        tried_moves = [child.move for child in self.children]
        untried_moves = [move for move in possible_moves if move not in tried_moves]
        if not untried_moves:
            return None
        move = random.choice(untried_moves)
        new_state = self.state.apply_move(move)
        child_node = Node(new_state, move, self)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        self.visits += 1
        self.wins += result

class MCTSAgent:
    def __init__(self, simulations=1000, time_limit=None):
        self.simulations = simulations
        self.time_limit = time_limit  # in Sekunden; falls None, wird simulations verwendet

    def make_move(self, game):
        """
        Wandelt den aktuellen Spielzustand in eine HexState um, baut den MCTS-Baum auf
        und gibt nach den Simulationen den besten Zug zurück.
        """
        root_state = HexState(game.matrix, game.current_player, game.num_emptyTiles, game.NUM_ROWS, game.NUM_COLS)
        root_node = Node(root_state)
        player = game.current_player  # Spieler, für den der Zug berechnet wird

        if self.time_limit is not None:
            end_time = time.time() + self.time_limit
            while time.time() < end_time:
                self.mcts_iteration(root_node, player)
        else:
            for _ in range(self.simulations):
                self.mcts_iteration(root_node, player)
        
        if root_node.children:
            best_child = max(root_node.children, key=lambda child: child.visits)
            return best_child.move
        else:
            # Fallback: Wähle einen zufälligen Zug, wenn keine Erweiterung erfolgt ist.
            possible_moves = root_state.get_possible_moves()
            return random.choice(possible_moves) if possible_moves else None

    def mcts_iteration(self, root, player):
        # SELECTION: Gehe entlang des Baumes
        node = root
        while node.children and node.is_fully_expanded():
            node = node.best_child(c_param=1.0, player=player)
        # EXPANSION: Falls der Knoten nicht terminal ist, erweitern wir den Baum
        if not node.state.is_terminal():
            child = node.expand()
            if child is not None:
                node = child
        # SIMULATION (Rollout) mit heuristikgestützter, epsilon-greedy Auswahl
        result = self.rollout(node.state, player)
        # BACKPROPAGATION: Ergebnisse zurück propagieren
        self.backpropagate(node, result, player)

    def rollout(self, state, player):
        current_state = state.clone()
        rollout_depth = 20  # Maximale Tiefe für Rollouts
        depth = 0
        epsilon = 0.2  # Wahrscheinlichkeit für einen rein zufälligen Zug
        while not current_state.is_terminal() and depth < rollout_depth:
            possible_moves = current_state.get_possible_moves()
            if not possible_moves:
                break
            if random.random() < epsilon:
                move = random.choice(possible_moves)
            else:
                best_eval = -float('inf')
                best_move = None
                for move_candidate in possible_moves:
                    next_state = current_state.apply_move(move_candidate)
                    eval_value = evaluate_state(next_state, player)
                    if eval_value > best_eval:
                        best_eval = eval_value
                        best_move = move_candidate
                move = best_move if best_move is not None else random.choice(possible_moves)
            current_state = current_state.apply_move(move)
            depth += 1
            current_eval = evaluate_state(current_state, player)
            if current_eval == float('inf'):
                return 1
            elif current_eval == -float('inf'):
                return 0
        if current_state.is_terminal():
            return 1 if current_state.check_win(player) else 0
        return 1 if evaluate_state(current_state, player) > 0 else 0

    def backpropagate(self, node, result, player):
        while node is not None:
            node.visits += 1
            if node.parent is not None:
                if node.parent.state.current_player != player:
                    node.wins += result
                else:
                    node.wins += (1 - result)
            else:
                node.wins += result
            node = node.parent
