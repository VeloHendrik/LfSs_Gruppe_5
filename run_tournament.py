from Game import Game
from agents.random_agent import make_random_move
from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent
import datetime
import time 

def play_match(agent_red, agent_blue):
    game = Game()
    game.current_player = 'red'
    max_moves = game.NUM_ROWS * game.NUM_COLS

    # Initialisiere KPIs: Zuganzahl und Rechenzeit 
    kpi = {
        "red": {"move_count": 0, "time": 0.0},
        "blue": {"move_count": 0, "time": 0.0}
    }
    
    for _ in range(max_moves):
        current_agent = agent_red if game.current_player == 'red' else agent_blue
        # Messe die Rechenzeit des Agenten
        start_time = time.time()
        move = current_agent(game)
        elapsed = time.time() - start_time
        
        kpi[game.current_player]["time"] += elapsed
        kpi[game.current_player]["move_count"] += 1
        
        if move:
            x, y = move
            game.matrix[y][x] = game.current_player.upper()[0]
            game.num_emptyTiles -= 1
            tile = game.grid.tiles[(x, y)]
            tile.colour = game.playerColours[game.current_player]
            
            # Die Simulation des Zeitverbrauchs wurde entfernt.
        else:
            return 'draw', kpi
        
        # Überprüfe, ob ein Spieler gewonnen hat.
        if game.findSolutionPath() is not None:
            return game.current_player, kpi
        
        game.changePlayer()
    
    return "draw", kpi

def write_bayesian_result(agent1_name, agent2_name, winner, round_number=None, kpi=None):
    date_str = datetime.date.today().strftime("%Y.%m.%d")
    if winner == 'red':
        result = "1-0"
    elif winner == 'blue':
        result = "0-1"
    else:
        result = "1/2-1/2"
    
    round_str = f"[Round \"{round_number}\"]\n" if round_number is not None else ""
    
    if kpi:
        red_moves = kpi["red"]["move_count"]
        blue_moves = kpi["blue"]["move_count"]
        red_time = f"{kpi['red']['time']:.2f}"
        blue_time = f"{kpi['blue']['time']:.2f}"
        kpi_fields = (
            f"[RedMoves \"{red_moves}\"]\n"
            f"[BlueMoves \"{blue_moves}\"]\n"
            f"[RedTime \"{red_time}\"]\n"
            f"[BlueTime \"{blue_time}\"]\n"
        )
    else:
        kpi_fields = ""
    
    record = (
        f"[Event \"Hex Tournament\"]\n"
        f"[Site \"Local\"]\n"
        f"[Date \"{date_str}\"]\n"
        f"{round_str}"
        f"[White \"{agent1_name}\"]\n"
        f"[Black \"{agent2_name}\"]\n"
        f"[Result \"{result}\"]\n"
        f"{kpi_fields}\n"
    )
    with open("bayesian_results.pgn", "a") as f:
        f.write(record)

def main():
    matches_per_pair = 5  # Anzahl der Matches pro Paarung
    results = []
    game_counter = 1  
    
    agent_dict = {
        'Random': make_random_move,
        'Minimax_depth2': lambda game: MinimaxAgent(depth=1).make_move(game),
        'MCTS': lambda game: MCTSAgent(simulations=1).make_move(game)
    }
    
    pairings = [
        ('Minimax_depth2', 'MCTS'),
        ('Random', 'MCTS'),
        ('Random', 'Minimax_depth2'),
    ]
    
    for agent1, agent2 in pairings:
        agent_red = agent_dict[agent1]
        agent_blue = agent_dict[agent2]
        
        for match_num in range(matches_per_pair):
            winner, kpi = play_match(agent_red, agent_blue)
            result_str = (
                f"{agent1} (red) vs {agent2} (blue) | Winner: {winner} | "
                f"red moves: {kpi['red']['move_count']}, blue moves: {kpi['blue']['move_count']} | "
                f"red time: {kpi['red']['time']:.2f}s, blue time: {kpi['blue']['time']:.2f}s"
            )
            print(result_str)
            results.append(result_str)
            # Speichere das Ergebnis im PGN-Format
            write_bayesian_result(agent1, agent2, winner, round_number=game_counter, kpi=kpi)
            game_counter += 1
    
    with open("tournament_results.txt", "w") as f:
        for line in results:
            f.write(line + "\n")

if __name__ == '__main__':
    main()
