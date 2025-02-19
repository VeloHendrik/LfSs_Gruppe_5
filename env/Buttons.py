import pygame
import consts

class Button:

    def __init__(self, display = None, pos = None, w=0, h=0,
                 bgColor=consts.THM_COLOR, selectedBgColor=consts.THM_LIGHT_COLOR,
                 text='', font='arial', fontDimension=26,
                 textColor=(0, 0, 0), value='', elevation = 0):

        if pos is None:
            pos = [0, 0]
        self.display = display
        self.bgColor = bgColor
        self.selectedBgColor = selectedBgColor
        self.text = text
        self.font = font
        self.pos = pos
        self.width = w
        self.height = h
        self.selected = False
        self.fontDimension = fontDimension
        self.textColor = textColor

        fontObj = pygame.font.SysFont(self.font, self.fontDimension)
        self.renderedText = fontObj.render(self.text, True, self.textColor)

        self.rectangle = pygame.Rect(pos, (w, h))
        self.bottom_rectangle = pygame.Rect(pos, (w, h))

        self.rectangleText = self.renderedText.get_rect(center=self.rectangle.center)
        self.value = value

    def select(self, selected):
        self.selected = selected
        self.draw()

    def selectByCoord(self, coord):
        if self.rectangle.collidepoint(coord):
            self.select(True)
            return True
        return False

    def updateRectangle(self):
        self.rectangle.left = self.pos[0]
        self.rectangle.top = self.pos[1]
        self.rectangleText = self.renderedText.get_rect(center=self.rectangle.center)

    def draw(self, btlradius=0, btrradius=0, bblradius=0, bbrradius=0):
        if self.selected:
            bgColor = self.selectedBgColor
        else:
            bgColor = self.bgColor

        if btlradius==0 and btrradius==0 and bblradius==0 and bbrradius==0:
            pygame.draw.rect(self.display, bgColor, self.rectangle, border_radius=0)
            pygame.draw.rect(self.display, consts.THM_COLOR, self.rectangle, width=2, border_radius=0)
        else:
            pygame.draw.rect(self.display, bgColor, self.rectangle, border_top_left_radius=btlradius,
                             border_top_right_radius=btrradius, border_bottom_left_radius=bblradius,
                             border_bottom_right_radius=bbrradius)
            pygame.draw.rect(self.display, consts.THM_COLOR, self.rectangle, width=2, border_top_left_radius=btlradius,
                             border_top_right_radius=btrradius, border_bottom_left_radius=bblradius,
                             border_bottom_right_radius=bbrradius)

        self.display.blit(self.renderedText, self.rectangleText)

class ButtonGroup:

    def __init__(self, buttonList=None, selected=0, space=0, top=0, left=0):
        if buttonList is None:
            buttonList = []
        self.buttonList = buttonList
        self.selected = selected
        self.buttonList[self.selected].selected = True
        self.top = top
        self.left = left

        currentLeft = self.left
        for button in self.buttonList:
            button.pos[1] = self.top
            button.pos[0] = currentLeft
            button.updateRectangle()
            currentLeft += space + button.width

    def selectByCoord(self, coord):
        for btnIndex, button in enumerate(self.buttonList):
            if button.selectByCoord(coord):
                if self.selected != btnIndex:
                    self.buttonList[self.selected].select(False)
                    self.selected = btnIndex
                    return True
        return False

    def draw(self):
        for idx, button in enumerate(self.buttonList):
            if idx == 0:
                button.draw(12,0,12,0)
            elif idx == len(self.buttonList)-1:
                button.draw(0,12,0,12)
            else:
                button.draw()

    def getValue(self):
        return self.buttonList[self.selected].value