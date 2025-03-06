import consts
import pygame
import sys
import startPage
from Game import Game
#from agents.random_agent import make_random_move
from agents.minimax_agent import make_minimax_move


if __name__ == '__main__':
    pygame.init()

    icon = pygame.image.load('../images/hex.png')
    pygame.display.set_caption("Hex Game")
    pygame.display.set_icon(icon)

    hexgame = Game()
    display = pygame.display.set_mode(size=hexgame.screenSize)

    hexgame.initialiseGame(display, hexgame)

    display.fill(consts.BACKGROUND_COLOR)
    startPlayer, gameMode = startPage.homePage(hexgame, display)

    hexgame.current_player = startPlayer
    hexgame.drawBoard()
    pygame.display.update()

    while hexgame.running:
        hexgame.drawBoard()
        pygame.display.update()

        # HUMAN VS AI (Blue ist KI)
        if gameMode == "human_ai" and hexgame.current_player == "blue":
            pygame.time.delay(500)
            move = make_minimax_move(hexgame, 2)
            if move:
                x, y = move
                tile = hexgame.grid.tiles[(x, y)]
            else:
                continue  # Keine Züge möglich
        else:
            # HUMAN MOVE
            move_made = False
            while not move_made:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        hexgame.running = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        if hexgame.quitButton.selectByCoord(mouse_pos):
                            hexgame.running = False
                            pygame.quit()
                            sys.exit(0)

                        tile = hexgame.getNearestTile(mouse_pos)
                        x, y = tile.gridPosition

                        if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                            move_made = True

        # Zug ausführen (gilt für Mensch und KI)
        if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
            tile.colour = hexgame.playerColours[hexgame.current_player]
            hexgame.matrix[y][x] = hexgame.current_player.upper()
            hexgame.grid.visitedTiles[tile.gridPosition] = 1
            hexgame.num_emptyTiles -= 1

            if hexgame.isGameOver():
                hexgame.text = 'Game over! {} wins!'.format(hexgame.current_player.capitalize())
                hexgame.drawBoard()
                pygame.display.update()
            else:
                hexgame.changePlayer()
                hexgame.text = hexgame.current_player.capitalize() + '\'s turn'

    # Ende-Schleife: Gewinnpfad endgültig zeichnen
    hexgame.drawBoard()
    pygame.display.update()

    # Warte auf Schließen des Fensters nach Spielende
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
