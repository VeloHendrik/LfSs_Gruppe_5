# agents/minimax_agent.py
import math
from agents.hex_state import HexState, evaluate_state

class MinimaxAgent:
    def __init__(self, depth=2):
        self.depth = depth

    def make_move(self, game):
        """
        Erzeugt aus dem aktuellen Spiel (game) einen simulierten Zustand
        und berechnet mittels Minimax den besten Zug.
        """
        state = HexState(game.matrix, game.current_player, game.num_emptyTiles, game.NUM_ROWS, game.NUM_COLS)
        best_move, _ = self.minimax(state, self.depth, -math.inf, math.inf, True, game.current_player)
        return best_move

    def minimax(self, state, depth, alpha, beta, maximizingPlayer, player):
        if depth == 0 or state.is_terminal():
            return None, evaluate_state(state, player)
        best_move = None
        if maximizingPlayer:
            max_eval = -math.inf
            for move in state.get_possible_moves():
                new_state = state.apply_move(move)
                _, eval = self.minimax(new_state, depth - 1, alpha, beta, False, player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = math.inf
            for move in state.get_possible_moves():
                new_state = state.apply_move(move)
                _, eval = self.minimax(new_state, depth - 1, alpha, beta, True, player)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval
