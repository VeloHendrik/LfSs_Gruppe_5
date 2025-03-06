import math
import sys
import pygame
import consts
from Buttons import *

buttonHeight = 50
algButtonWidth = 170
playerButtonWidth = 100
startButtonWidth = 110
difficultyButtonWidth = 200
gametypeButtonWidth = 300
topMargin = 60


def homePage(game, display):
    player = ButtonGroup(
        top=2 * topMargin + buttonHeight,
        left=game.screenSize[0] / 2 - playerButtonWidth,
        buttonList=[
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Red", value="red",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=playerButtonWidth, h=buttonHeight,
                   text="Blue", value="blue",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK)
        ],
        selected=0
    )

    gameType = ButtonGroup(
        top=3*topMargin + 2*buttonHeight,
        left=game.screenSize[0] / 2 - gametypeButtonWidth / 2,
        buttonList=[
            Button(display=display, w=gametypeButtonWidth//2, h=buttonHeight,
                   text="Human vs Human", value="human_human",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=gametypeButtonWidth//2, h=buttonHeight,
                   text="Human vs AI", value="human_ai",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK)
        ],
        selected=0
    )

    start = Button(display=display,
                   pos=[game.screenSize[0] / 2 - startButtonWidth / 2, 5*topMargin + buttonHeight],
                   w=startButtonWidth,
                   h=buttonHeight,
                   textColor=consts.BLACK,
                   text="Start")

    quitbtn = Button(display=display,
                     pos=[game.screenSize[0] / 2 - startButtonWidth / 2, 5*topMargin + 2*buttonHeight + 35],
                     w=startButtonWidth,
                     h=buttonHeight,
                     textColor=consts.BLACK,
                     text="Quit")

    text = "Welcome to the Game Hex. Please choose from the following options"
    fontObj = pygame.font.SysFont('arial', 40)
    renderedText = fontObj.render(text, True, (255, 255, 255))
    width = 800
    height = 100
    left = game.screenSize[0] / 2 - width / 2
    top = topMargin
    rectangle = pygame.Rect(left, top, width, height)
    rectangleText = renderedText.get_rect(center=rectangle.center)
    pygame.draw.rect(game.display, game.backgroundColor, rectangle)
    game.display.blit(renderedText, rectangleText)

    player.draw()
    gameType.draw()
    start.draw(12,12,12,12)
    quitbtn.draw(12,12,12,12)
    game.drawTHMLogo()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if quitbtn.selectByCoord(pos):
                    pygame.quit()
                    sys.exit(0)
                player.selectByCoord(pos)
                gameType.selectByCoord(pos)

                if start.selectByCoord(pos):
                    return player.getValue(), gameType.getValue()
        pygame.display.update()
