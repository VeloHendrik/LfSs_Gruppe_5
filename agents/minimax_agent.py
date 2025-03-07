import math
import copy
import heapq

class MinimaxAgent:
    def __init__(self, depth=20):
        """
        depth: Suchtiefe (in ply, also Halbzüge; z. B. depth=15 entspricht ca. 7-8 Zügen pro Seite)
        """
        self.depth = depth
        self.transposition_table = {}

    def board_to_tuple(self, matrix):
        """Konvertiert das Brett (2D-Liste) in ein Tuple, um es als Schlüssel zu verwenden."""
        return tuple(tuple(row) for row in matrix)

    def copy_board(self, matrix):
        """Effiziente Kopie eines 2D-Arrays (Brett)."""
        return [row[:] for row in matrix]

    def get_possible_moves(self, matrix):
        """Gibt alle freien Felder als Liste von (x, y)-Tupeln zurück."""
        moves = []
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x] == '.':
                    moves.append((x, y))
        return moves

    def is_game_over(self, matrix):
        """Das Spiel ist vorbei, wenn keine freien Felder mehr vorhanden sind."""
        return len(self.get_possible_moves(matrix)) == 0

    def shortest_path_length(self, matrix, player):
        """
        Berechnet mittels Dijkstra den minimalen "Weg" für den Spieler,
        um seine Zielränder zu verbinden:
         - Für Blue (B): von der linken zur rechten Seite.
         - Für Red (R): von der oberen zur unteren Seite.
        Eigene Steine zählen mit geringen Kosten, leere Felder mit moderaten,
        und gegnerische Felder sind teuer.
        """
        n = len(matrix)
        costs = [[math.inf] * n for _ in range(n)]
        heap = []
        # Initialisierung: Quelle sind die Zellen am entsprechenden Startrand
        if player == 'B':
            for y in range(n):
                if matrix[y][0] == player:
                    cost = 0
                elif matrix[y][0] == '.':
                    cost = 1
                else:
                    cost = 100
                costs[y][0] = cost
                heapq.heappush(heap, (cost, (0, y)))
            target_check = lambda x, y: x == n - 1
        else:  # player == 'R'
            for x in range(n):
                if matrix[0][x] == player:
                    cost = 0
                elif matrix[0][x] == '.':
                    cost = 1
                else:
                    cost = 100
                costs[0][x] = cost
                heapq.heappush(heap, (cost, (x, 0)))
            target_check = lambda x, y: y == n - 1

        # Definiere die 6 möglichen Nachbarn (Hex-Richtungen)
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]
        while heap:
            cost, (x, y) = heapq.heappop(heap)
            if cost > costs[y][x]:
                continue
            if target_check(x, y):
                return cost
            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    if matrix[ny][nx] == player:
                        new_cost = cost  # Eigener Stein: keine Zusatzkosten
                    elif matrix[ny][nx] == '.':
                        new_cost = cost + 1  # Leeres Feld: moderate Kosten
                    else:
                        new_cost = cost + 100  # Gegnerischer Stein: hohe Kosten
                    if new_cost < costs[ny][nx]:
                        costs[ny][nx] = new_cost
                        heapq.heappush(heap, (new_cost, (nx, ny)))
        return math.inf

    def evaluate_board(self, matrix, player):
        """
        Bewertet das Brett anhand der minimalen Verbindungswege:
         - Berechnet die kürzeste Verbindung (Wegkosten) für den Spieler
           und den Gegner.
         - Ein niedriger Wert ist besser.
         - Der Score entspricht der Differenz:
             opponent_distance - player_distance.
           (Je größer diese Differenz, desto besser steht der Spieler da.)
        """
        opponent = 'R' if player == 'B' else 'B'
        player_distance = self.shortest_path_length(matrix, player)
        opponent_distance = self.shortest_path_length(matrix, opponent)
        
        # Gewinnbedingung: Erreicht der Spieler das Ziel, wird ein hoher positiver Wert zurückgegeben.
        if player_distance == 0:
            return 1000
        if opponent_distance == 0:
            return -1000
        
        return opponent_distance - player_distance

    def minimax(self, matrix, depth, alpha, beta, maximizingPlayer, player):
        """
        Führt den Minimax-Algorithmus mit Alpha-Beta-Pruning aus.
         - matrix: aktueller Spielzustand (2D-Liste)
         - depth: verbleibende Suchtiefe
         - alpha, beta: Werte für das Pruning
         - maximizingPlayer: True, wenn der aktuelle Zug maximiert werden soll (eigener Spieler),
           False, wenn der Gegner (Minimierer) am Zug ist.
         - player: der eigene Spieler ('B' oder 'R')
        
        Gibt ein Tupel (Wert, Zug) zurück.
        """
        board_key = (self.board_to_tuple(matrix), depth, maximizingPlayer)
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]
        
        if depth == 0 or self.is_game_over(matrix):
            value = self.evaluate_board(matrix, player)
            self.transposition_table[board_key] = (value, None)
            return value, None

        moves = self.get_possible_moves(matrix)
        # --- Move Ordering: sortiere Züge anhand einer schnellen Heuristik ---
        ordered_moves = []
        if maximizingPlayer:
            for move in moves:
                new_matrix = self.copy_board(matrix)
                new_matrix[move[1]][move[0]] = player
                eval_val = self.evaluate_board(new_matrix, player)
                ordered_moves.append((move, eval_val))
            ordered_moves.sort(key=lambda x: x[1], reverse=True)
        else:
            opponent = 'R' if player == 'B' else 'B'
            for move in moves:
                new_matrix = self.copy_board(matrix)
                new_matrix[move[1]][move[0]] = opponent
                eval_val = self.evaluate_board(new_matrix, player)
                ordered_moves.append((move, eval_val))
            ordered_moves.sort(key=lambda x: x[1])
        # --------------------------------------------------------

        best_move = None

        if maximizingPlayer:
            max_eval = -math.inf
            for move, _ in ordered_moves:
                new_matrix = self.copy_board(matrix)
                new_matrix[move[1]][move[0]] = player
                eval_score, _ = self.minimax(new_matrix, depth - 1, alpha, beta, False, player)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta-Pruning
            self.transposition_table[board_key] = (max_eval, best_move)
            return max_eval, best_move
        else:
            min_eval = math.inf
            opponent = 'R' if player == 'B' else 'B'
            for move, _ in ordered_moves:
                new_matrix = self.copy_board(matrix)
                new_matrix[move[1]][move[0]] = opponent
                eval_score, _ = self.minimax(new_matrix, depth - 1, alpha, beta, True, player)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self.transposition_table[board_key] = (min_eval, best_move)
            return min_eval, best_move

    def make_move(self, game):
        """
        Führt iterative Deepening durch, beginnend mit Tiefe 1 bis self.depth.
        Erwartet ein Spielobjekt, das mindestens die Attribute
         - game.matrix (2D-Liste des Bretts)
         - game.current_player (String, z. B. "blue" oder "red")
        enthält.
        
        Gibt den besten gefundenen Zug als (x, y)-Tupel zurück.
        """
        player = game.current_player.upper()[0]
        best_move = None
        for d in range(1, self.depth + 1):
            self.transposition_table.clear()  # Transpositionstabelle leeren
            score, move = self.minimax(game.matrix, d, -math.inf, math.inf, True, player)
            if move is not None:
                best_move = move
        return best_move
