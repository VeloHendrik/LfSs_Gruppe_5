# tournament.py
from Game import Game
from agents.random_agent import make_random_move
from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent
import datetime

def play_match(agent_red, agent_blue, time_limit=300):
    game = Game()
    game.current_player = 'red'
    max_moves = game.NUM_ROWS * game.NUM_COLS
    # Initialisiere Timer für beide Spieler (in Sekunden)
    game.timers = {'red': time_limit, 'blue': time_limit}
    
    for _ in range(max_moves):
        if game.current_player == 'red':
            move = agent_red(game)
        else:
            move = agent_blue(game)
        
        if move:
            x, y = move
            # Aktualisiere das Spielfeld: Matrix und Grid
            game.matrix[y][x] = game.current_player.upper()[0]
            game.num_emptyTiles -= 1
            
            # Setze auch das Tile im Grid, damit Gewinnabfrage funktioniert.
            tile = game.grid.tiles[(x, y)]
            tile.colour = game.playerColours[game.current_player]
            
            # Simuliere den Zeitverbrauch: 1 Sekunde pro Zug
            game.timers[game.current_player] -= 1  
            if game.timers[game.current_player] <= 0:
                # Zeit abgelaufen – Gegner gewinnt
                return 'red' if game.current_player == 'blue' else 'blue'
        else:
            return 'draw'
        
        # Überprüfe, ob ein Spieler gewonnen hat.
        if game.findSolutionPath() is not None:
            return game.current_player
        
        game.changePlayer()
    
    return "draw"

def write_bayesian_result(agent1_name, agent2_name, winner, round_number=None):
    date_str = datetime.date.today().strftime("%Y.%m.%d")
    # Mapping: "red" entspricht White, "blue" entspricht Black.
    if winner == 'red':
        result = "1-0"
    elif winner == 'blue':
        result = "0-1"
    else:
        result = "1/2-1/2"
    
    round_str = f"[Round \"{round_number}\"]\n" if round_number is not None else ""
    
    record = (
        f"[Event \"Hex Tournament\"]\n"
        f"[Site \"Local\"]\n"
        f"[Date \"{date_str}\"]\n"
        f"{round_str}"
        f"[White \"{agent1_name}\"]\n"
        f"[Black \"{agent2_name}\"]\n"
        f"[Result \"{result}\"]\n\n"
    )
    with open("bayesian_results.pgn", "a") as f:
        f.write(record)

def main():
    matches_per_pair = 5  # Beispiel: 5 Matches pro Paarung
    results = []
    game_counter = 1  # Zähler für die Rundennummer
    
    # Agenten als Funktionen: Jeweils wird eine neue Instanz des jeweiligen Agenten erstellt.
    agent_dict = {
        'Random': make_random_move,
        'Minimax_depth2': lambda game: MinimaxAgent(depth=2).make_move(game),
        'MCTS': lambda game: MCTSAgent(simulations=20).make_move(game)
    }
    
    pairings = [
        ('Random', 'MCTS'),
        ('Random', 'Minimax_depth2'),
        ('Minimax_depth2', 'MCTS'),
    ]
    
    time_limit = 3000000000  # Sekunden pro Spieler
    
    for agent1, agent2 in pairings:
        agent_red = agent_dict[agent1]
        agent_blue = agent_dict[agent2]
        
        for match_num in range(matches_per_pair):
            winner = play_match(agent_red, agent_blue, time_limit=time_limit)
            result_str = f"{agent1} (red) vs {agent2} (blue) | Winner: {winner}"
            print(result_str)
            results.append(result_str)
            # Speichere das Ergebnis im PGN-Format; game_counter wird als Rundennummer verwendet.
            write_bayesian_result(agent1, agent2, winner, round_number=game_counter)
            game_counter += 1
    
    # Optional: Schreibe zusätzlich alle Turnierergebnisse in eine separate Datei.
    with open("tournament_results.txt", "w") as f:
        for line in results:
            f.write(line + "\n")

if __name__ == '__main__':
    main()
