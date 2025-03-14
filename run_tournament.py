# tournament.py
from Game import Game
from agents.random_agent import make_random_move
from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent
import datetime
import string


def pos_to_hex_notation(x, y):
    """Wandelt die (x, y)-Position in Hex-Notation um (A1, B2 etc.)."""
    return f"{string.ascii_uppercase[x]}{y+1}"


def play_match(agent_red, agent_blue, time_limit=300):
    game = Game()
    game.current_player = 'red'
    max_moves = game.NUM_ROWS * game.NUM_COLS
    move_list = []  # Speichert alle Züge für das PGN-Format
    game.timers = {'red': time_limit, 'blue': time_limit}

    for move_num in range(max_moves):
        if game.current_player == 'red':
            move = agent_red(game)
        else:
            move = agent_blue(game)

        if move:
            x, y = move
            game.matrix[y][x] = game.current_player.upper()[0]
            game.num_emptyTiles -= 1
            tile = game.grid.tiles[(x, y)]
            tile.colour = game.playerColours[game.current_player]
            move_list.append((move_num + 1, pos_to_hex_notation(x, y)))  # Nummerierter Zug

            game.timers[game.current_player] -= 1
            if game.timers[game.current_player] <= 0:
                return ('red' if game.current_player == 'blue' else 'blue'), move_list
        else:
            return "draw", move_list

        if game.findSolutionPath() is not None:
            return game.current_player, move_list

        game.changePlayer()

    return "draw", move_list


def write_bayesian_result(agent1_name, agent2_name, winner, moves, round_number=None):
    date_str = datetime.date.today().strftime("%Y.%m.%d")
    result_map = {'red': "1-0", 'blue': "0-1", 'draw': "1/2-1/2"}
    result = result_map.get(winner, "1/2-1/2")

    round_str = f"[Round \"{round_number}\"]\n" if round_number is not None else ""

    move_text = " ".join([f"{num}. {move}" for num, move in moves])  # Formatiere Züge

    record = (
        f"[Event \"Hex Tournament\"]\n"
        f"[Site \"Local\"]\n"
        f"[Date \"{date_str}\"]\n"
        f"{round_str}"
        f"[White \"{agent1_name}\"]\n"
        f"[Black \"{agent2_name}\"]\n"
        f"[Result \"{result}\"]\n\n"
        f"{move_text}\n\n"
    )

    with open("bayesian_results.pgn", "a") as f:
        f.write(record)


def main():
    matches_per_pair = 30
    results = []
    game_counter = 1
    agent_dict = {
        'Random': make_random_move,
        'Minimax_depth2': lambda game: MinimaxAgent(depth=2).make_move(game),
        'MCTS': lambda game: MCTSAgent(simulations=20).make_move(game)
    }

    pairings = [
        ('Random', 'Minimax_depth2'),
        ('Minimax_depth2', 'MCTS'),
        ('Random', 'MCTS'),
       
    ]

    time_limit = 3000000000

    for agent1, agent2 in pairings:
        agent_red = agent_dict[agent1]
        agent_blue = agent_dict[agent2]

        for match_num in range(matches_per_pair):
            winner, moves = play_match(agent_red, agent_blue, time_limit=time_limit)
            result_str = f"{agent1} (red) vs {agent2} (blue) | Winner: {winner}"
            print(result_str)
            results.append(result_str)
            write_bayesian_result(agent1, agent2, winner, moves, round_number=game_counter)
            game_counter += 1

    with open("tournament_results.txt", "w") as f:
        for line in results:
            f.write(line + "\n")


if __name__ == '__main__':
    main()
