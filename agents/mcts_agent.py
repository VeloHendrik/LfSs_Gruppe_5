import math
import random
import copy

class Node:
    """
    Repräsentiert einen Knoten im MCTS-Baum.
    - state_matrix: 2D-Liste (Brettzustand)
    - current_player: 'B' oder 'R'
    - parent: Referenz auf Elternknoten
    - children: Liste der Kindknoten
    - untried_moves: Liste der möglichen Züge, die von diesem Knoten noch nicht expandiert wurden
    - visits: Anzahl der Besuche
    - wins: Anzahl der Siege (aus Sicht des Spielers, der diesen Knoten 'erzeugt' hat)
    """
    def __init__(self, state_matrix, current_player, parent=None):
        self.state_matrix = state_matrix
        self.current_player = current_player  # Wer ist in diesem Zustand am Zug?
        self.parent = parent
        self.children = []
        self.untried_moves = []
        self.visits = 0
        self.wins = 0
    
    def __repr__(self):
        return f"<Node p={self.current_player} visits={self.visits} wins={self.wins} children={len(self.children)}>"


class MCTSAgent:
    def __init__(self, simulations=1000):
        """
        simulations: Anzahl der MCTS-Simulationen pro Zug.
        """
        self.simulations = simulations
    
    def copy_board(self, matrix):
        """Schnelles Kopieren des Brettzustands."""
        return [row[:] for row in matrix]

    def get_possible_moves(self, matrix):
        """Liste aller freien Felder (x, y)."""
        moves = []
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x] == '.':
                    moves.append((x, y))
        return moves

    def is_game_over(self, matrix):
        """
        Gibt True zurück, wenn das Spiel beendet ist.
        Hier als Beispiel: keine freien Felder => Spielende.
        Besser wäre es, auf einen echten Hex-Gewinner zu prüfen.
        """
        return len(self.get_possible_moves(matrix)) == 0

    def get_winner(self, matrix):
        """
        Bestimmt den Gewinner (z. B. 'B', 'R' oder None).
        Für ein echtes Hex-Spiel solltest du hier die
        Durchgangsprüfung (z. B. BFS) implementieren.
        """
        # Platzhalter: Wenn keine Züge mehr => unentschieden (None).
        # In Hex gibt es zwar kein klassisches Unentschieden,
        # aber du musst hier deinen BFS/DS/Algorithmus einbinden.
        if self.is_game_over(matrix):
            # (Beispiel: zufälliger "Gewinner")
            return random.choice(['B', 'R'])
        return None

    def do_move(self, matrix, player, move):
        """Führt einen Zug (x, y) auf dem Brett aus."""
        new_matrix = self.copy_board(matrix)
        x, y = move
        new_matrix[y][x] = player
        return new_matrix

    def switch_player(self, player):
        return 'R' if player == 'B' else 'B'

    def expand_node(self, node):
        """
        Wählt einen noch nicht expandierten Zug aus node.untried_moves,
        erzeugt das entsprechende Kind und gibt es zurück.
        """
        move = node.untried_moves.pop()
        next_state = self.do_move(node.state_matrix, node.current_player, move)
        child_player = self.switch_player(node.current_player)
        child_node = Node(next_state, child_player, parent=node)
        node.children.append(child_node)
        return child_node, move

    def ucb_score(self, child, parent_visits, c_param=1.4142):
        """
        Berechnet den Upper Confidence Bound (UCB1).
        child.wins: Siege aus Sicht des Spielers, der diesen Child-Knoten erzeugt hat
        child.visits: wie oft dieser Child besucht wurde
        parent_visits: wie oft der Elternknoten besucht wurde
        c_param: explorationskonstante
        """
        if child.visits == 0:
            return float('inf')  # noch unbesucht => Favorisieren
        win_rate = child.wins / child.visits
        exploration = math.sqrt(math.log(parent_visits) / child.visits)
        return win_rate + c_param * exploration

    def select_child(self, node):
        """
        Wählt das Kind mit dem höchsten UCB-Score.
        """
        best_child = max(node.children, key=lambda c: self.ucb_score(c, node.visits))
        return best_child

    def rollout(self, matrix, current_player):
        """
        Simuliert zufällig das Spiel bis zum Ende.
        Gibt den Gewinner zurück ('B' oder 'R' oder None).
        Du kannst hier eine bessere Policy implementieren,
        statt rein zufällige Züge zu spielen.
        """
        # Kopie des Zustands
        state = self.copy_board(matrix)
        player = current_player

        # Spiele, bis Spielende
        while not self.is_game_over(state):
            possible_moves = self.get_possible_moves(state)
            move = random.choice(possible_moves)
            state = self.do_move(state, player, move)
            player = self.switch_player(player)
        
        winner = self.get_winner(state)
        return winner

    def backpropagate(self, node, winner):
        """
        Backpropagation:
        Gehe vom Endknoten zurück bis zur Wurzel
        und aktualisiere visits und wins.
        """
        while node is not None:
            node.visits += 1
            # Falls der Gewinner mit dem Spieler übereinstimmt,
            # der diesen Knoten "besitzt", zähle es als Sieg
            # (Je nach Definition: Node.current_player oder parent.current_player)
            # Hier: wir interpretieren "wins" aus Sicht des vorherigen Spielers
            # => also der, der den Zug gemacht hat.
            # Du kannst das anpassen, falls du es anders tracken möchtest.
            prev_player = self.switch_player(node.current_player)
            if winner == prev_player:
                node.wins += 1
            node = node.parent

    def mcts_search(self, root_node, time_steps):
        """
        Führt 'time_steps' Simulationen aus, beginnend bei root_node.
        """
        for _ in range(time_steps):
            node = root_node

            # 1) SELECTION: gehe so lange zu den bereits expandierten Kindern
            #               bis wir bei einem Knoten mit unversuchten Zügen
            #               oder bei einem Endzustand landen.
            while node.untried_moves == [] and node.children:
                node = self.select_child(node)

            # 2) EXPANSION: wenn untried_moves vorhanden sind, expandiere
            if node.untried_moves:
                node, move = self.expand_node(node)

            # 3) SIMULATION (Rollout)
            winner = self.rollout(node.state_matrix, node.current_player)

            # 4) BACKPROPAGATION
            self.backpropagate(node, winner)

    def make_move(self, game):
        """
        Erzeugt einen MCTS-Baum aus dem aktuellen Spielzustand
        und wählt am Ende den Zug mit der höchsten win_rate.
        """
        # 1) Erstelle den Wurzelknoten
        #    Wir nehmen an, game.matrix ist eine 2D-Liste
        #    und game.current_player ist "blue" oder "red".
        #    => wir mappen "blue" -> 'B' und "red" -> 'R'
        current_player = game.current_player.upper()[0]
        root = Node(
            state_matrix=self.copy_board(game.matrix),
            current_player=current_player,
            parent=None
        )

        # 2) Erzeuge die initialen untried_moves
        root.untried_moves = self.get_possible_moves(root.state_matrix)

        # 3) Starte MCTS
        self.mcts_search(root, self.simulations)

        # 4) Wähle das Kind mit der höchsten Siegrate
        if not root.children:
            # Keine Kinder => Keine Züge => None
            return None

        best_child = max(
            root.children,
            key=lambda c: c.wins / c.visits if c.visits > 0 else 0
        )

        # best_child repräsentiert den Zustand NACH dem Zug.
        # Um den eigentlichen Zug (x, y) zu bekommen, können wir
        # in best_child.state_matrix mit root.state_matrix vergleichen.
        move_played = None
        for y in range(len(root.state_matrix)):
            for x in range(len(root.state_matrix[0])):
                if root.state_matrix[y][x] == '.' and best_child.state_matrix[y][x] != '.':
                    move_played = (x, y)
                    break
            if move_played is not None:
                break

        return move_played
