import consts
import pygame
import sys
import startPage

from Game import Game


if __name__ == '__main__':
    pygame.init()

    icon = pygame.image.load('../images/hex.png')
    pygame.display.set_caption("Hex Game")
    pygame.display.set_icon(icon)

    hexgame = Game()
    display = pygame.display.set_mode(size=hexgame.screenSize)

    hexgame.initialiseGame(display, hexgame)

    display.fill(consts.BACKGROUND_COLOR)
    startPlayer = startPage.homePage(hexgame, display)

    hexgame.current_player = startPlayer
    hexgame.drawBoard()
    pygame.display.update()

    while hexgame.running:
        hexgame.drawBoard()
        events = pygame.event.get()

        for event in events:
            # if the x is pressed in pygame window
            if event.type == pygame.QUIT:
                hexgame.running = False
                pygame.quit()

            # if the mouse is pressed with left-click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # if the quit button is pressed during game
                if hexgame.quitButton.selectByCoord(mouse_pos):
                    hexgame.running = False
                    pygame.quit()
                    sys.exit(0)

                # make move
                tile = hexgame.getNearestTile(mouse_pos)
                x,y = tile.gridPosition

                # check whether tile is empty and game is not over yet
                if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                    tile.colour = hexgame.playerColours[hexgame.current_player]
                    # update logic in game, that is, matrix, visitedTiles and number of emptyTiles
                    hexgame.matrix[y][x] = hexgame.current_player.upper()
                    hexgame.grid.visitedTiles[tile.gridPosition] = 1
                    hexgame.num_emptyTiles -= 1


                    if hexgame.isGameOver():
                        hexgame.text = 'Game over! {} wins!'.format(hexgame.current_player.capitalize())
                    else:
                        # change the player
                        hexgame.changePlayer()
                        hexgame.text = hexgame.current_player.capitalize() + '\'s turn'

                    # update the screen
                    hexgame.drawBoard()
                    pygame.display.update()

