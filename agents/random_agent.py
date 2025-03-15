import random


def make_random_move(game):
    empty_tiles = [
        (x, y) for y in range(game.NUM_ROWS)
        for x in range(game.NUM_COLS)
        if game.matrix[y][x] == game.EMPTY
    ]

    if empty_tiles:
        return random.choice(empty_tiles)
    else:
        return None
