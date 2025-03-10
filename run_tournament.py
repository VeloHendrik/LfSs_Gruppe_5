# tournament.py
from Game import Game
from agents.random_agent import make_random_move
from agents.minimax_agent import make_minimax_move
from agents.mcts_agent import make_mcts_move

def play_match(agent_red, agent_blue, depth_red=2, depth_blue=2, simulations_red=100, simulations_blue=100, time_limit=300):
    game = Game()
    game.current_player = 'red'
    max_moves = game.NUM_ROWS * game.NUM_COLS
    # Initialisiere Timer für beide Spieler (in Sekunden)
    game.timers = {'red': time_limit, 'blue': time_limit}
    
    for _ in range(max_moves):
        if game.current_player == 'red':
            if agent_red == make_random_move:
                move = agent_red(game)
            elif agent_red == make_minimax_move:
                move = agent_red(game, depth_red)
            elif agent_red == make_mcts_move:
                move = agent_red(game, simulations=simulations_red)
        else:
            if agent_blue == make_random_move:
                move = agent_blue(game)
            elif agent_blue == make_minimax_move:
                move = agent_blue(game, depth_blue)
            elif agent_blue == make_mcts_move:
                move = agent_blue(game, simulations=simulations_blue)

        if move:
            x, y = move
            game.matrix[y][x] = game.current_player.upper()[0]
            game.num_emptyTiles -= 1
            # Simuliere den Zeitverbrauch pro Zug (hier 1 Sekunde)
            game.timers[game.current_player] -= 1
            if game.timers[game.current_player] <= 0:
                # Aktueller Spieler hat keine Zeit mehr – Gegner gewinnt
                return 'red' if game.current_player == 'blue' else 'blue'
        else:
            return 'draw'

        if game.findSolutionPath() is not None:
            return game.current_player

        game.changePlayer()

    return "draw"

def main():
    matches_per_pair = 5  # Beispielweise wenige Matches zum Testen
    results = []

    agent_dict = {
        'Random': make_random_move,
        'Minimax_depth2': make_minimax_move,
        'MCTS': make_mcts_move
    }

    pairings = [
        ('Random', 'Minimax_depth2'),
        ('Random', 'MCTS'),
        ('Minimax_depth2', 'MCTS'),
    ]

    # Setze ein Zeitlimit für jeden Spieler (z. B. 300 Sekunden)
    time_limit = 300

    for agent1, agent2 in pairings:
        agent_red = agent_dict[agent1]
        agent_blue = agent_dict[agent2]

        for match_num in range(matches_per_pair):
            winner = play_match(agent_red, agent_blue, time_limit=time_limit)
            result_str = f"{agent1} (red) vs {agent2} (blue) | Winner: {winner}"
            print(result_str)
            results.append(result_str)

    with open("tournament_results.txt", "w") as f:
        for line in results:
            f.write(line + '\n')

if __name__ == '__main__':
    main()
