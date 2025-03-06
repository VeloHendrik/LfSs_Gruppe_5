import random


def make_random_move(game):
    """
    Selects a random move from all available empty tiles.

    Parameters:
    - game (Game): Die aktuelle Instanz des Spiels.

    Returns:
    - (x, y): Koordinaten des ausgewählten zufälligen Spielzugs.
    """
    empty_tiles = [
        (x, y) for y in range(game.NUM_ROWS)
        for x in range(game.NUM_COLS)
        if game.matrix[y][x] == game.EMPTY
    ]

    if empty_tiles:
        return random.choice(empty_tiles)
    else:
        return None
