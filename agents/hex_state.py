from collections import deque
import heapq

class HexState:
    def __init__(self, matrix, current_player, num_empty, NUM_ROWS, NUM_COLS):
        """
        :param matrix: Spielfeld als 2D-Liste
        :param current_player: Aktueller Spieler ('red' oder 'blue')
        :param num_empty: Anzahl der leeren Felder
        :param NUM_ROWS: Anzahl der Reihen
        :param NUM_COLS: Anzahl der Spalten
        """
        # Erstelle eine Kopie des Spielfelds, um Änderungen nicht global zu machen
        self.matrix = [row[:] for row in matrix]
        self.current_player = current_player
        self.num_empty = num_empty
        self.NUM_ROWS = NUM_ROWS
        self.NUM_COLS = NUM_COLS

    def clone(self):
        # Erstellt eine Kopie des aktuellen Zustands.
        return HexState(self.matrix, self.current_player, self.num_empty, self.NUM_ROWS, self.NUM_COLS)

    def get_possible_moves(self):
        # Gibt eine Liste aller möglichen Spielzüge zurück (Positionen der leeren Felder).
        moves = []
        for y in range(self.NUM_ROWS):
            for x in range(self.NUM_COLS):
                if self.matrix[y][x] == '.':
                    moves.append((x, y))
        return moves

    def apply_move(self, move):
        # Wendet einen Spielzug an und gibt den neuen Zustand zurück.
        x, y = move
        new_state = self.clone()
        new_state.matrix[y][x] = new_state.current_player.upper()[0]  # Setzt das Feld auf den Buchstaben des Spielers
        new_state.num_empty -= 1  # Reduziert die Anzahl der leeren Felder
        new_state.current_player = 'blue' if new_state.current_player == 'red' else 'red'  # Wechselt den Spieler
        return new_state

    def is_terminal(self):
        # Überprüft, ob das Spiel beendet ist (ein Spieler hat gewonnen oder keine Züge mehr möglich sind)
        return self.check_win("red") or self.check_win("blue") or self.num_empty == 0

    def check_win(self, player):
        # Prüft, ob der angegebene Spieler gewonnen hat (Verbindung von einer Seite zur anderen)
        mark = player.upper()[0]  
        visited = [[False for _ in range(self.NUM_COLS)] for _ in range(self.NUM_ROWS)]
        q = deque()
        
        if player == "red":  # Rot muss von oben nach unten verbinden
            for x in range(self.NUM_COLS):
                if self.matrix[0][x] == mark:
                    q.append((x, 0))
                    visited[0][x] = True
            while q:
                cx, cy = q.popleft()
                if cy == self.NUM_ROWS - 1:
                    return True  
                for nx, ny in self.get_neighbors(cx, cy):
                    if not visited[ny][nx] and self.matrix[ny][nx] == mark:
                        visited[ny][nx] = True
                        q.append((nx, ny))
        else:  # Blau muss von links nach rechts verbinden
            for y in range(self.NUM_ROWS):
                if self.matrix[y][0] == mark:
                    q.append((0, y))
                    visited[y][0] = True
            while q:
                cx, cy = q.popleft()
                if cx == self.NUM_COLS - 1:
                    return True  
                for nx, ny in self.get_neighbors(cx, cy):
                    if not visited[ny][nx] and self.matrix[ny][nx] == mark:
                        visited[ny][nx] = True
                        q.append((nx, ny))
        return False

    def get_neighbors(self, x, y):
        # Gibt die Nachbarn eines Feldes zurück
        moves = []
        if x > 0 and y < self.NUM_ROWS - 1:
            moves.append((x - 1, y + 1))
        if y < self.NUM_ROWS - 1:
            moves.append((x, y + 1))
        if x > 0:
            moves.append((x - 1, y))
        if x < self.NUM_COLS - 1:
            moves.append((x + 1, y))
        if y > 0:
            moves.append((x, y - 1))
        if x < self.NUM_COLS - 1 and y > 0:
            moves.append((x + 1, y - 1))
        return moves

def shortest_path_distance(state, player):
    """
    Berechnet mittels Dijkstra (Priority Queue) eine Schätzung des minimalen „Abstands“ vom Start- zum Zielrand.
    """
    mark = player.upper()[0]
    INF = 10**6  # Sehr großer Wert für nicht erreichbare Felder
    dist = [[INF for _ in range(state.NUM_COLS)] for _ in range(state.NUM_ROWS)]
    pq = []  # Priority Queue für Dijkstra

    if player == "red":
        for x in range(state.NUM_COLS):
            if state.matrix[0][x] in [mark, '.']:
                cost = 0 if state.matrix[0][x] == mark else 1
                dist[0][x] = cost
                heapq.heappush(pq, (cost, (x, 0)))
    else:
        for y in range(state.NUM_ROWS):
            if state.matrix[y][0] in [mark, '.']:
                cost = 0 if state.matrix[y][0] == mark else 1
                dist[y][0] = cost
                heapq.heappush(pq, (cost, (0, y)))
    
    while pq:
        current_cost, (cx, cy) = heapq.heappop(pq)
        if current_cost > dist[cy][cx]:
            continue
        for nx, ny in state.get_neighbors(cx, cy):
            if state.matrix[ny][nx] not in [mark, '.']:
                continue
            cost = 0 if state.matrix[ny][nx] == mark else 1
            if dist[ny][nx] > current_cost + cost:
                dist[ny][nx] = current_cost + cost
                heapq.heappush(pq, (dist[ny][nx], (nx, ny)))
    
    return min(dist[state.NUM_ROWS - 1][x] for x in range(state.NUM_COLS)) if player == "red" else min(dist[y][state.NUM_COLS - 1] for y in range(state.NUM_ROWS))

def evaluate_state(state, player):
    #Bewertet den Zustand anhand der Distanzwerte. 
    if state.is_terminal():
        if state.check_win(player):
            return float('inf')
        elif state.check_win("red" if player == "blue" else "blue"):
            return -float('inf')
        return 0
    return shortest_path_distance(state, "blue" if player == "red" else "red") - shortest_path_distance(state, player)
