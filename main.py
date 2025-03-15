import consts
import pygame
import sys
import startPage
from Game import Game
from agents.minimax_agent import MinimaxAgent
from agents.mcts_agent import MCTSAgent
from agents.random_agent import random
from Buttons import Button 

def main():
    pygame.init()
    icon = pygame.image.load('./images/hex.png')
    pygame.display.set_caption("Hex Game")
    pygame.display.set_icon(icon)
    display = pygame.display.set_mode(size=(1280, 720))
    
    while True:
        hexgame = Game()
        hexgame.initialiseGame(display, hexgame)
        display.fill(consts.BACKGROUND_COLOR)
        
        result = startPage.homePage(hexgame, display)
        startPlayer = result[0]
        gameMode = result[1]
        time_limit = result[2]
        if gameMode == "human_ai":
            ai_opponent = result[3]
        else:
            ai_opponent = None

        hexgame.timers = {'red': time_limit, 'blue': time_limit}
        hexgame.current_player = startPlayer
        hexgame.show_elo = False
        hexgame.drawBoard()
        pygame.display.update()
        
        clock = pygame.time.Clock()
        hexgame.running = True
        
        toggleEloButton = Button(
            display=display,
           pos=[20, hexgame.screenSize[1] - 200],
            w=200,
            h=50,
            text="(geht noch nicht)",
            bgColor=consts.THM_COLOR,
            selectedBgColor=consts.THM_LIGHT_COLOR,
            textColor=consts.WHITE
        )
        
        while hexgame.running:
            dt = clock.tick(30) / 1000.0  
            if hexgame.timers[hexgame.current_player] != float('inf'):
                hexgame.timers[hexgame.current_player] -= dt
                if hexgame.timers[hexgame.current_player] <= 0:
                    loser = hexgame.current_player
                    winner = 'blue' if loser == 'red' else 'red'
                    hexgame.text = "Time's up! {} wins!".format(winner.capitalize())
                    hexgame.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    # Prüfe den Quit-Button
                    if hexgame.quitButton.selectByCoord(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    # Prüfe den Toggle-Elo-Button
                    if toggleEloButton.selectByCoord(mouse_pos):
                        hexgame.show_elo = not hexgame.show_elo
                    # Prüfe Eingabe eines Spielers:
                    if gameMode == "human_human" or (gameMode == "human_ai" and hexgame.current_player == "red"):
                        tile = hexgame.getNearestTile(mouse_pos)
                        x, y = tile.gridPosition
                        if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                            hexgame.human_move = (x, y)

            # KI-Zug im Human-vs-AI-Modus
            if gameMode == "human_ai" and hexgame.current_player == "blue":
                pygame.time.delay(500)
                if ai_opponent == "minimax":
                    agent = MinimaxAgent()
                elif ai_opponent == "mcts":
                    agent = MCTSAgent()
                elif ai_opponent == "random":
                    agent = random()
                else:
                    agent = MinimaxAgent()  # Fallback
                move = agent.make_move(hexgame)
                if move:
                    hexgame.human_move = move

            if hasattr(hexgame, 'human_move'):
                x, y = hexgame.human_move
                if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                    tile = hexgame.grid.tiles[(x, y)]
                    tile.colour = hexgame.playerColours[hexgame.current_player]
                    hexgame.matrix[y][x] = hexgame.current_player.upper()[0]
                    hexgame.grid.visitedTiles[tile.gridPosition] = 1
                    hexgame.num_emptyTiles -= 1

                    # Letzten Zug speichern zum hervorheben
                    hexgame.last_move = (x, y)

                    if hexgame.isGameOver():
                        hexgame.text = 'Game over! {} wins!'.format(hexgame.current_player.capitalize())
                        hexgame.running = False
                    else:
                        hexgame.changePlayer()
                        hexgame.text = hexgame.current_player.capitalize() + "'s turn"
                del hexgame.human_move

            hexgame.drawBoard()
            toggleEloButton.draw(12, 12, 12, 12)
            pygame.display.update()
        
        restartButton = Button(
            display=display,
            pos=[hexgame.screenSize[0] - 150 - 20, 20 + 50 + 10],  
            w=150,
            h=50,
            text="Restart",
            bgColor=consts.THM_COLOR,
            selectedBgColor=consts.THM_LIGHT_COLOR,
            textColor=consts.WHITE
        )
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if hexgame.quitButton.selectByCoord(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    if restartButton.selectByCoord(mouse_pos):
                        restartButton.selected = True
                        break
            hexgame.drawBoard()  
            restartButton.draw(12, 12, 12, 12)
            pygame.display.update()
            clock.tick(30)
            if restartButton.selected:
                break

if __name__ == '__main__':
    main()
