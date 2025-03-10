# Game.py
import consts
import pygame
import sys
import copy
from HexBoard import Grid
from Buttons import Button

class Game:
    EMPTY = '.'

    def __init__(self, matrix=None):
        self.backgroundColor = consts.BACKGROUND_COLOR
        self.screenSize = (1280, 720)
        self.boardPosition = (250, 80)
        self.tileSize = 30
        self.NUM_ROWS = 11
        self.NUM_COLS = 11
        self.grid = Grid(self.NUM_ROWS, self.NUM_COLS, self.tileSize)
        self.num_emptyTiles = self.NUM_ROWS * self.NUM_COLS
        self.emptyColour = (70, 70, 70)
        self.playerColours = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255)
        }
        self.current_player = None
        self.running = True
        for tile in self.hexTiles():
            tile.colour = self.emptyColour
        self.matrix = matrix or [[self.__class__.EMPTY for _ in range(self.NUM_COLS)] for _ in range(self.NUM_ROWS)]
        self.text = "Red's turn"
        self.solution = None
        self.quitButton = None
        # Timer wird später gesetzt (kann float('inf') sein für "No Limit")
        self.timers = {'red': 0, 'blue': 0}

    @classmethod
    def initialiseGame(cls, display, game):
        cls.display = display
        cls.tileSize = game.tileSize

    def hexTiles(self):
        return self.grid.tiles.values()

    def getNearestTile(self, pos):
        nearestTile = None
        minDist = sys.maxsize
        for tile in self.hexTiles():
            distance = tile.distanceSq(pos, self.boardPosition)
            if distance < minDist:
                minDist = distance
                nearestTile = tile
        return nearestTile

    def changePlayer(self):
        self.current_player = 'blue' if self.current_player == 'red' else 'red'

    def findSolutionPath(self):
        for tile in self.grid.topRow():
            if tile.colour == self.playerColours['red']:
                path = self.grid.findPath(tile, self.grid.bottomRow(), self.playerColours['red'])
                if path is not None:
                    return path
        for tile in self.grid.leftColumn():
            if tile.colour == self.playerColours['blue']:
                path = self.grid.findPath(tile, self.grid.rightColumn(), self.playerColours['blue'])
                if path is not None:
                    return path
        return None

    def isGameOver(self):
        if self.solution is None:
            self.solution = self.findSolutionPath()
        return self.solution is not None

    def showMatrix(self):
        for row in self.matrix:
            print(" ".join(row))

    def showText(self):
        fontObj = pygame.font.SysFont('arial', 40)
        renderedText = fontObj.render(self.text, True, (255, 255, 255))
        width = 400
        height = 100
        left = self.screenSize[0] / 2 - width / 2
        top = self.screenSize[1] - 1.3 * height
        rectangle = pygame.Rect(left, top, width, height)
        rectangleText = renderedText.get_rect(center=rectangle.center)
        pygame.draw.rect(self.display, self.backgroundColor, rectangle)
        self.display.blit(renderedText, rectangleText)

    def drawTimers(self):
        # Falls beide Timer unendlich sind, wird nichts angezeigt.
        if self.timers['red'] == float('inf') and self.timers['blue'] == float('inf'):
            return
        fontObj = pygame.font.SysFont('arial', 30)
        red_time = max(0, int(self.timers['red'])) if self.timers['red'] != float('inf') else "∞"
        blue_time = max(0, int(self.timers['blue'])) if self.timers['blue'] != float('inf') else "∞"
        red_text = fontObj.render(f"Red: {red_time}s", True, self.playerColours['red'])
        blue_text = fontObj.render(f"Blue: {blue_time}s", True, self.playerColours['blue'])
        self.display.blit(red_text, (20, 20))
        self.display.blit(blue_text, (20, 20 + red_text.get_height() + 5))

    def drawTile(self, tile):
        corners = tile.cornerPoints(self.boardPosition)
        pygame.draw.polygon(self.display, tile.colour, corners)
        pygame.draw.polygon(self.display, (50, 50, 50), corners, 5)
        pygame.draw.polygon(self.display, (255, 255, 255), corners, 3)
        if self.solution and tile in self.solution:
            pygame.draw.polygon(self.display, (255, 215, 0), corners, 6)

    def drawBoard(self):
        self.display.fill(self.backgroundColor)
        for tile in self.hexTiles():
            self.drawTile(tile)
        self.showText()
        self.drawTimers()
        self.drawBorder()
        self.drawQuitButton()
        self.drawTHMLogo()

    def drawBorder(self):
        colours = list(self.playerColours.values())
        colour1 = colours[0]
        colour2 = colours[1]
        width = 4
        self.drawOneSideBorder(colour1, self.grid.topRow(), 3, 6, width)
        self.drawOneSideBorder(colour1, self.grid.bottomRow(), 0, 3, width)
        self.drawOneSideBorder(colour2, self.grid.leftColumn(), 1, 4, width)
        self.drawOneSideBorder(colour2, self.grid.rightColumn(), 4, 1, width)

    def drawOneSideBorder(self, colour, row, fromPoint, toPoint, width):
        for tile in row:
            corners = tile.cornerPoints(self.boardPosition)
            if fromPoint >= toPoint:
                corners = corners[fromPoint:] + corners[:toPoint]
            else:
                corners = corners[fromPoint:toPoint]
            pygame.draw.lines(self.display, colour, False, corners, width)

    def drawQuitButton(self):
        buttonWidth = 150
        buttonHeight = 50
        self.quitButton = Button(
            display=self.display,
            pos=[self.screenSize[0] - buttonWidth - 20, 20],
            w=buttonWidth,
            h=buttonHeight,
            text="QUIT",
            bgColor=consts.THM_COLOR,
            selectedBgColor=consts.THM_LIGHT_COLOR,
            fontDimension=26,
            textColor=consts.WHITE
        )
        # Runde Ecken: 12 Pixel an allen Ecken
        self.quitButton.draw(12, 12, 12, 12)

    def drawTHMLogo(self):
        logo = pygame.image.load("./images/logo.png")
        scaled_logo = pygame.transform.scale(logo, (210, 70))
        self.display.blit(scaled_logo, (20, self.screenSize[1] - 90))
