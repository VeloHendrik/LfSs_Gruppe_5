import random
import copy

def get_possible_moves(matrix):
    return [(x, y) for y in range(len(matrix))
            for x in range(len(matrix[0]))
            if matrix[y][x] == '.']

def apply_move(matrix, move, player):
    new_matrix = [row[:] for row in matrix]
    new_matrix[move[1]][move[0]] = player
    return new_matrix

def random_playout(matrix, player):
    moves = get_possible_moves(matrix)
    while moves:
        move = random.choice(moves)
        matrix = apply_move(matrix, move, player)
        moves = get_possible_moves(matrix)
        player = 'R' if player == 'B' else 'B'
    # hier könntest du eine Gewinnprüfung durchführen, momentan random
    return random.choice([True, False])

def make_mcts_move(game, simulations=100):
    player = game.current_player.upper()[0]
    moves = get_possible_moves(game.matrix)
    best_move = None
    best_score = -1

    for move in moves:
        wins = 0
        for _ in range(simulations):
            new_matrix = apply_move(game.matrix, move, player)
            if random_playout(copy.deepcopy(new_matrix), player):
                wins += 1
        score = wins / simulations
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
