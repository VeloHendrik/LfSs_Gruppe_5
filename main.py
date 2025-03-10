# main.py
import consts
import pygame
import sys
import startPage
from Game import Game
from agents.mcts_agent import MCTSAgent
from Buttons import Button  # Für den Restart-Button

def main():
    pygame.init()
    icon = pygame.image.load('./images/hex.png')
    pygame.display.set_caption("Hex Game")
    pygame.display.set_icon(icon)
    display = pygame.display.set_mode(size=(1280, 720))
    
    # Äußere Schleife: Nach jedem Spiel kehren wir ins Hauptmenü zurück.
    while True:
        # Neues Spielobjekt anlegen und Startseite anzeigen
        hexgame = Game()
        hexgame.initialiseGame(display, hexgame)
        display.fill(consts.BACKGROUND_COLOR)
        
        # Starte die Startseite; erst wenn "Start" gedrückt wird, kehrt sie zurück.
        startPlayer, gameMode, time_limit = startPage.homePage(hexgame, display)
        # Setze beide Timer auf das gewählte Zeitlimit (in Sekunden)
        hexgame.timers = {'red': time_limit, 'blue': time_limit}
        hexgame.current_player = startPlayer
        hexgame.drawBoard()
        pygame.display.update()
        
        # Jetzt initialisieren wir den Clock neu – ab hier läuft die eigentliche Spielzeit.
        clock = pygame.time.Clock()
        hexgame.running = True
        
        while hexgame.running:
            dt = clock.tick(30) / 1000.0  # dt in Sekunden
            # Aktualisiere den Timer nur, wenn kein "No Limit" eingestellt wurde.
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
                    # Prüfe den integrierten Quit-Button (wird in hexgame.drawQuitButton gezeichnet)
                    if hexgame.quitButton.selectByCoord(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    # Im Human-vs-Human-Modus oder im Human-vs-AI-Modus, wenn "red" (Mensch) an der Reihe ist:
                    if gameMode == "human_human" or (gameMode == "human_ai" and hexgame.current_player == "red"):
                        tile = hexgame.getNearestTile(mouse_pos)
                        x, y = tile.gridPosition
                        if hexgame.matrix[y][x] == hexgame.EMPTY and not hexgame.isGameOver():
                            hexgame.human_move = (x, y)

            # KI-Zug im Human-vs-AI-Modus
            if gameMode == "human_ai" and hexgame.current_player == "blue":
                pygame.time.delay(500)
                agent = MCTSAgent(simulations=20)
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

                    if hexgame.isGameOver():
                        hexgame.text = 'Game over! {} wins!'.format(hexgame.current_player.capitalize())
                        hexgame.running = False
                    else:
                        hexgame.changePlayer()
                        hexgame.text = hexgame.current_player.capitalize() + "'s turn"
                del hexgame.human_move

            hexgame.drawBoard()
            pygame.display.update()
        
        # Nach Spielende: Endbildschirm mit Restart-Button (Quit-Button bleibt integriert)
        # Der Quit-Button wird in hexgame.drawQuitButton() (z. B. oben rechts) gezeichnet.
        # Wir erstellen einen Restart-Button, der direkt unter dem Quit-Button angezeigt wird.
        restartButton = Button(
            display=display,
            pos=[hexgame.screenSize[0] - 150 - 20, 20 + 50 + 10],  # direkt unter Quit-Button
            w=150,
            h=50,
            text="Restart",
            bgColor=consts.THM_COLOR,
            selectedBgColor=consts.THM_LIGHT_COLOR,
            textColor=consts.WHITE
        )
        
        # End-Schleife: Hier wird der Bildschirm (inklusive Quit-Button) neu gezeichnet und zusätzlich der Restart-Button angezeigt.
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
            hexgame.drawBoard()  # Zeichnet u.a. auch den integrierten Quit-Button
            restartButton.draw(12, 12, 12, 12)
            pygame.display.update()
            clock.tick(30)
            if restartButton.selected:
                break

if __name__ == '__main__':
    main()
