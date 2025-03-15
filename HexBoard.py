import math

class Tile:
    """
    A class to represent a single pointy-top oriented tile.
    Details on geometry can be found here:
    https://www.redblobgames.com/grids/hexagons/#basics
    ...

    Attributes
    ----------
    gridPosition: tuple
        row and column of the tile in the grid
    width: int
        width of the tile
    height: int
        height of the tile
    neighbours: list
        list of all neighbouring tiles this tile belongs to. This will be filled by the grid init

    """
    def __init__(self, row: int, column: int, size: float) -> None:
        self.gridPosition = (row, column)
        self.width, self.height = self.__computeDimensions(size)
        self.neighbours = []

    def __str__(self):
        return f'{self.gridPosition}'

    def __repr__(self):
        return f'HexTile{self.gridPosition}'

    def __computeDimensions(self, size):
        """
        Computes the width and height of the tile. Since it is pointy-top oriented the width is sqrt(3)*size

        :param size:    size of the tile
        :return:        width and height of the tile
        """
        return size * math.sqrt(3), size * 2

    def centerPoint(self, offset=(0, 0)):
        """
        Calculates the center point of the tile depending on an offset. Here, it is considered
        that the board is an odd-row layout with a parallelogram as board

        :param offset:
        :return:
        """
        x, y = self.gridPosition
        dx, dy = offset
        height = math.floor(self.height * 3 / 4)

        # each second row is shifted by half of the width since it is an odd-row horizontal layout
        if y % 2:
            dx += self.width // 2
        x += y // 2 # this is necessary to have the parallelogram structure of the board game
        return x * self.width + dx, y * height + dy

    def cornerPoint(self, radius, index, pos):
        """
        Calculates the corner point of the tile with index i

        :param radius:  radius of the outer circle of the tile
        :param index:   index of the corner point starting with 0 a top right corner
        :param pos:     position of the tile
        :return:        x-,y- coordinates of the corner point
        """
        deg = 60 * index + 30
        theta = math.pi / 180 * deg
        x, y = pos
        return radius * math.cos(theta) + x, radius * math.sin(theta) + y

    def cornerPoints(self, offset=(0, 0)):
        """
        Calculates the six corner points of the tile starting from right top corner point counter-clockwise

        :param offset:
        :return:        list of corner points of the tile
        """
        radius = self.height // 2
        position_px = self.centerPoint(offset)
        return [self.cornerPoint(radius, i, position_px) for i in range(6)]

    def distanceSq(self, position, offset):
        """
        calculates the squared distance of the position and the center point of the tile

        :param position:    position to calc the distance from
        :param offset:      offset of the center point
        :return:            distance of the position to the center point
        """
        p1 = self.centerPoint(offset)
        p2 = position
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x1 - x2, y2 - y1
        return dx * dx + dy * dy

class Grid:
    """
    A class that represents the grid of the game.

    Attributes
    __________
    height: int
        the number of tiles in the height direction of the grid
    width: int
        the number of tiles in the width direction of the grid
    tiles: dict with tuples as key and Tiles as value
        collections of the tiles with coordinate tuples
    visitedTiles: dict with tuples as key and a boolean value
        boolean value is 1 if the tiles is visited else 0
    matrix: list (two-dimensional)
        matrix for string representation of the grid
    """
    EMPTY = '.'
    
    def __init__(self, height: int, width: int, tileSize: float) -> None:
        self.height = height
        self.width = width
        self.tiles = {(x, y): Tile(x, y, tileSize) for x in range(width) for y in range(height)}
        self.visitedTiles = {(x, y): 0 for x in range(width) for y in range(height)}

        self.matrix = [[self.__class__.EMPTY for _ in range(self.width)] for _ in range(self.height)]

        for tile in self.tiles.values():
            self.findNeighbours(tile)
    
    def __str__(self):
        text = ''
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                if j == 0:
                    text += ' ' * i
                text += str(row[j])+ '  '
            text += '\n'
        return text

    def findNeighbours(self, tile: Tile) -> None:
        """"
            finds all neighbours of the tile and saves it in the neighbours attribut of the tile class

        :param tile:    the tile to find neighbours for
        :return:        None
        """
        x, y = tile.gridPosition

        if x > 0 and y < self.height - 1:
            tile.neighbours.append(self.tiles[(x - 1, y + 1)])
        if y < self.height - 1:
            tile.neighbours.append(self.tiles[(x, y + 1)])
        if x > 0:
            tile.neighbours.append(self.tiles[(x - 1, y)])
        if x < self.width - 1:
            tile.neighbours.append(self.tiles[(x + 1, y)])
        if y > 0:
            tile.neighbours.append(self.tiles[(x, y - 1)])
        if x < self.width - 1 and y > 0:
            tile.neighbours.append(self.tiles[(x + 1, y - 1)])

    def topRow(self):
        return [self.tiles[(x, 0)] for x in range(self.width)]

    def bottomRow(self):
        return [self.tiles[(x, self.height - 1)] for x in range(self.width)]

    def leftColumn(self):
        return [self.tiles[(0, y)] for y in range(self.height)]

    def rightColumn(self):
        return [self.tiles[(self.width - 1, y)] for y in range(self.height)]

    def findPath(self, fromTile, toTileList, playerColour, visited=None):
        if visited is None:
            visited = []

        if fromTile.colour != playerColour:
            return None
        if fromTile in visited:
            return None

        if fromTile in toTileList:
            return [fromTile]

        visited.append(fromTile)

        for neighbour in fromTile.neighbours:
            path = self.findPath(neighbour, toTileList, playerColour, visited)
            if path is not None:
                path.append(fromTile)
                return path

        return None
    