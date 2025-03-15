#!/usr/bin/env python3
from Game import Game
from agents.random_agent import make_random_move
from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent
import datetime
import time
import concurrent.futures
import os

def play_match(agent_red, agent_blue, time_limit=300):
    game = Game()
    game.current_player = 'red'
    max_moves = game.NUM_ROWS * game.NUM_COLS
    # Initialisiere Timer für beide Spieler (in Sekunden)
    game.timers = {'red': time_limit, 'blue': time_limit}
    
    # Initialisiere KPI-Tracking: Zuganzahl und Rechenzeit (in Sekunden)
    kpi = {
        "red": {"move_count": 0, "time": 0.0},
        "blue": {"move_count": 0, "time": 0.0}
    }
    
    for _ in range(max_moves):
        # Bestimme den aktuellen Agenten
        current_agent = agent_red if game.current_player == 'red' else agent_blue
        
        # Messe die Rechenzeit des Agenten
        start_time = time.time()
        move = current_agent(game)
        elapsed = time.time() - start_time
        
        # Update der KPIs für den aktuellen Spieler
        kpi[game.current_player]["time"] += elapsed
        kpi[game.current_player]["move_count"] += 1
        
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
                return ('red' if game.current_player == 'blue' else 'blue'), kpi
        else:
            return 'draw', kpi
        
        # Überprüfe, ob ein Spieler gewonnen hat.
        if game.findSolutionPath() is not None:
            return game.current_player, kpi
        
        game.changePlayer()
    
    return "draw", kpi

def write_bayesian_result(agent1_name, agent2_name, winner, round_number=None, kpi=None):
    date_str = datetime.date.today().strftime("%Y.%m.%d")
    # Mapping: "red" entspricht White, "blue" entspricht Black.
    if winner == 'red':
        result = "1-0"
    elif winner == 'blue':
        result = "0-1"
    else:
        result = "1/2-1/2"
    
    round_str = f"[Round \"{round_number}\"]\n" if round_number is not None else ""
    
    # Zusätzliche KPI-Felder, sofern vorhanden
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

# Agenten als top-level Funktionen, damit sie in Worker-Prozessen funktionieren
def agent_random(game):
    return make_random_move(game)

def agent_minimax_depth2(game):
    # Beachte: wie im Originalcode wird hier depth=1 verwendet.
    return MinimaxAgent(depth=2).make_move(game)

def agent_mcts(game):
    return MCTSAgent(simulations=10).make_move(game)

# Diese Funktion wird in den Worker-Prozessen aufgerufen.
def run_match(task):
    agent1, agent2, time_limit = task
    # Erstelle das Agenten-Dictionary lokal (sodass es picklable ist)
    agent_dict = {
        'Random': agent_random,
        'Minimax_depth2': agent_minimax_depth2,
        'MCTS': agent_mcts
    }
    agent_red = agent_dict[agent1]
    agent_blue = agent_dict[agent2]
    winner, kpi = play_match(agent_red, agent_blue, time_limit=time_limit)
    return (agent1, agent2, winner, kpi)

def main():
    matches_per_pair = 5  # Anzahl Matches pro Paarung
    results = []
    game_counter = 1  # Zähler für die Rundennummer
    
    pairings = [
        ('Minimax_depth2', 'MCTS'),
        ('Random', 'MCTS'),
        ('Random', 'Minimax_depth2'),
    ]
    
    time_limit = 3000000000  # Sekunden pro Spieler
    tasks = []
    for pairing in pairings:
        for _ in range(matches_per_pair):
            tasks.append((pairing[0], pairing[1], time_limit))
    
    # Parallele Ausführung der Matches
    max_workers = os.cpu_count() // 2

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        results_parallel = list(executor.map(run_match, tasks))
    
    for agent1, agent2, winner, kpi in results_parallel:
        result_str = (
            f"{agent1} (red) vs {agent2} (blue) | Winner: {winner} | "
            f"red moves: {kpi['red']['move_count']}, blue moves: {kpi['blue']['move_count']} | "
            f"red time: {kpi['red']['time']:.2f}s, blue time: {kpi['blue']['time']:.2f}s"
        )
        print(result_str)
        write_bayesian_result(agent1, agent2, winner, round_number=game_counter, kpi=kpi)
        results.append(result_str)
        game_counter += 1
    
    with open("tournament_results.txt", "w") as f:
        for line in results:
            f.write(line + "\n")

if __name__ == '__main__':
    main()
