import math
from agents.hex_state import HexState, evaluate_state

class MinimaxAgent:
    def __init__(self, depth=2):
        self.depth = depth

    def make_move(self, game):
        """
        Erzeugt aus dem aktuellen Spiel (game) einen simulierten Zustand.
        Falls ein direkter Gewinnzug (für den Agenten) möglich ist, wird dieser direkt gewählt.
        Andernfalls wird mittels Minimax der beste Zug berechnet.
        Falls Minimax keinen Zug zurückgibt (z.B. weil alle Züge sehr schlecht sind),
        wird als Fallback der erste verfügbare Zug gewählt.
        """
        state = HexState(game.matrix, game.current_player, game.num_emptyTiles, game.NUM_ROWS, game.NUM_COLS)
        
        # Prüfe, ob ein direkter Gewinnzug möglich ist
        for move in state.get_possible_moves():
            new_state = state.apply_move(move)
            if new_state.is_terminal():
                return move

        best_move, _ = self.minimax(state, self.depth, -math.inf, math.inf, True, game.current_player)
        if best_move is None:
            # Fallback: Wähle den ersten möglichen Zug
            possible_moves = state.get_possible_moves()
            if possible_moves:
                best_move = possible_moves[0]
        return best_move

    def minimax(self, state, depth, alpha, beta, maximizingPlayer, player):
        if depth == 0 or state.is_terminal():
            return None, evaluate_state(state, player)
        
        moves = state.get_possible_moves()
        # Falls keine Züge möglich sind, wird direkt der Heuristik-Wert zurückgegeben.
        if not moves:
            return None, evaluate_state(state, player)
        
        # Move-Ordering: Sortiere die Züge anhand der heuristischen Bewertung.
        moves = sorted(
            moves, 
            key=lambda move: evaluate_state(state.apply_move(move), player), 
            reverse=maximizingPlayer
        )
        
        best_move = moves[0]  # Setze als initialen Fallback den ersten Zug aus der Liste.
        
        if maximizingPlayer:
            max_eval = -math.inf
            for move in moves:
                new_state = state.apply_move(move)
                _, eval = self.minimax(new_state, depth - 1, alpha, beta, False, player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return best_move, max_eval
        else:
            min_eval = math.inf
            for move in moves:
                new_state = state.apply_move(move)
                _, eval = self.minimax(new_state, depth - 1, alpha, beta, True, player)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return best_move, min_eval
