import math
import copy

def evaluate_board(matrix, player):
    score = 0
    opponent = 'R' if player == 'B' else 'B'

    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == player[0]:
                center_distance = abs(x - len(matrix)//2) + abs(y - len(matrix)//2)
                score += max(10 - center_distance, 1)
            elif matrix[y][x] == opponent:
                score -= 1
    return score

def get_possible_moves(matrix):
    return [(x, y) for y in range(len(matrix))
            for x in range(len(matrix[0]))
            if matrix[y][x] == '.']

def is_game_over(matrix):
    return len(get_possible_moves(matrix)) == 0

def minimax(matrix, depth, alpha, beta, maximizingPlayer, player):
    if depth == 0 or is_game_over(matrix):
        return evaluate_board(matrix, player), None

    moves = get_possible_moves(matrix)
    best_move = None

    if maximizingPlayer:
        maxEval = -math.inf
        for move in moves:
            new_matrix = copy.deepcopy(matrix)
            new_matrix[move[1]][move[0]] = player[0]
            eval, _ = minimax(new_matrix, depth-1, alpha, beta, False, player)
            if eval > maxEval:
                maxEval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = math.inf
        opponent = 'R' if player == 'B' else 'B'
        for move in moves:
            new_matrix = copy.deepcopy(matrix)
            new_matrix[move[1]][move[0]] = opponent
            eval, _ = minimax(new_matrix, depth-1, alpha, beta, True, player)
            if eval < minEval:
                minEval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move

def make_minimax_move(game, depth):
    _, best_move = minimax(game.matrix, depth, -math.inf, math.inf, True, game.current_player.upper()[0])
    return best_move
