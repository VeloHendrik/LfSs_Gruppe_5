import pygame
import sys
from Buttons import ButtonGroup, Button
import consts

def parse_time(input_str):
    """
    Wandelt einen String in Sekunden um.
    Erlaubte Formate: mm:ss oder nur mm.
    Liefert None bei ungültiger Eingabe.
    """
    input_str = input_str.strip()
    if ':' in input_str:
        parts = input_str.split(':')
        if len(parts) != 2:
            return None
        try:
            minutes = int(parts[0])
            seconds = int(parts[1])
            if seconds >= 60 or seconds < 0 or minutes < 0:
                return None
            return minutes * 60 + seconds
        except ValueError:
            return None
    else:
        try:
            minutes = int(input_str)
            if minutes < 0:
                return None
            return minutes * 60
        except ValueError:
            return None

def homePage(game, display):
    # Grundlayout-Parameter
    topMargin = 60
    spacing = 20
    buttonHeight = 50
    screenWidth, screenHeight = game.screenSize

    # Titel und Instruktionen
    title_font = pygame.font.SysFont('arial', 50)
    title_text = "Welcome to Hex Game"
    title_surface = title_font.render(title_text, True, consts.WHITE)
    
    instr_font = pygame.font.SysFont('arial', 30)
    instr_text = "Please select your options:"
    instr_surface = instr_font.render(instr_text, True, consts.WHITE)
    
    # Berechne Positionen
    title_y = topMargin
    instr_y = title_y + title_surface.get_height() + 10
    
    # Spieler-Auswahlgruppe
    playerGroupY = instr_y + instr_surface.get_height() + spacing
    playerButtonWidth = 100
    player = ButtonGroup(
        top=playerGroupY,
        left=screenWidth / 2 - playerButtonWidth,
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
    
    # Spielmodus-Auswahlgruppe
    gametypeButtonWidth = 450
    gameTypeY = playerGroupY + buttonHeight + spacing
    gameType = ButtonGroup(
        top=gameTypeY,
        left=screenWidth / 2 - gametypeButtonWidth / 2,
        buttonList=[
            Button(display=display, w=gametypeButtonWidth // 2, h=buttonHeight,
                   text="Human vs Human", value="human_human",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=gametypeButtonWidth // 2, h=buttonHeight,
                   text="Human vs AI", value="human_ai",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK)
        ],
        selected=0
    )
    
    # Zeitlimit-Auswahlgruppe (5 Buttons: "No Limit", "1:00", "3:00", "5:00" und "Custom")
    timeButtonWidth = 100
    timeLimitLeft = screenWidth / 2 - (timeButtonWidth * 5 + 40) / 2
    timeLimitY = gameTypeY + buttonHeight + spacing
    timeLimit = ButtonGroup(
        top=timeLimitY,
        left=timeLimitLeft,
        buttonList=[
            Button(display=display, w=timeButtonWidth, h=buttonHeight,
                   text="No Limit", value="nolimit",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=timeButtonWidth, h=buttonHeight,
                   text="1:00", value=60,
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=timeButtonWidth, h=buttonHeight,
                   text="3:00", value=180,
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=timeButtonWidth, h=buttonHeight,
                   text="5:00", value=300,
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK),
            Button(display=display, w=timeButtonWidth, h=buttonHeight,
                   text="Custom", value="custom",
                   bgColor=consts.THM_COLOR,
                   selectedBgColor=consts.WHITE,
                   textColor=consts.BLACK)
        ],
        selected=0  # Default ist "No Limit"
    )
    
    # Start- und Quit-Buttons (Positionen werden später dynamisch gesetzt)
    startButtonWidth = 110
    start = Button(display=display,
                   pos=[screenWidth / 2 - startButtonWidth / 2, timeLimitY + buttonHeight + spacing + 60],
                   w=startButtonWidth,
                   h=buttonHeight,
                   textColor=consts.BLACK,
                   text="Start")
    
    quitbtn = Button(display=display,
                     pos=[screenWidth / 2 - startButtonWidth / 2, timeLimitY + buttonHeight + spacing + 60 + buttonHeight + spacing],
                     w=startButtonWidth,
                     h=buttonHeight,
                     textColor=consts.BLACK,
                     text="Quit")
    
    # Initiales Zeichnen
    display.fill(consts.BACKGROUND_COLOR)
    display.blit(title_surface, (screenWidth / 2 - title_surface.get_width() / 2, title_y))
    display.blit(instr_surface, (screenWidth / 2 - instr_surface.get_width() / 2, instr_y))
    player.draw()
    gameType.draw()
    timeLimit.draw()
    start.draw(12, 12, 12, 12)
    quitbtn.draw(12, 12, 12, 12)
    game.drawTHMLogo()
    
    # Variablen für Custom-Zeit-Eingabe
    custom_input_text = ""
    input_active = False
    error_message = ""
    custom_input_y = timeLimitY + buttonHeight + spacing + 10

    aiSelection = None  # Für die Auswahl des KI-Gegners

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(30) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if quitbtn.selectByCoord(pos):
                    pygame.quit()
                    sys.exit()
                player.selectByCoord(pos)
                gameType.selectByCoord(pos)
                timeLimit.selectByCoord(pos)
                # Wenn Human vs AI gewählt ist, auch KI-Auswahl berücksichtigen
                if gameType.getValue() == "human_ai" and aiSelection is not None:
                    aiSelection.selectByCoord(pos)
                # Aktiviere Eingabe, falls "Custom" gewählt wurde
                if timeLimit.getValue() == "custom":
                    input_active = True
                else:
                    input_active = False
                    custom_input_text = ""
                if start.selectByCoord(pos):
                    val = timeLimit.getValue()
                    if val == "custom":
                        seconds = parse_time(custom_input_text)
                        if seconds is None:
                            error_message = "Invalid format! Use mm:ss or mm."
                            continue
                        else:
                            time_limit = seconds
                    elif val == "nolimit":
                        time_limit = float('inf')
                    else:
                        time_limit = val
                    if gameType.getValue() == "human_ai":
                        # Stelle sicher, dass aiSelection existiert
                        if aiSelection is None:
                            error_message = "Please select an AI opponent!"
                            continue
                        return player.getValue(), gameType.getValue(), time_limit, aiSelection.getValue()
                    else:
                        return player.getValue(), gameType.getValue(), time_limit
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    custom_input_text = custom_input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    seconds = parse_time(custom_input_text)
                    if seconds is None:
                        error_message = "Invalid custom time format!"
                    else:
                        error_message = ""
                else:
                    if event.unicode.isdigit() or event.unicode == ":":
                        custom_input_text += event.unicode
        
        # Aktualisiere dynamisch die Position der Start- und Quit-Buttons
        if gameType.getValue() == "human_ai":
            current_startY = timeLimitY + buttonHeight + spacing + buttonHeight + spacing + 60
        else:
            current_startY = timeLimitY + buttonHeight + spacing + 60
        start.pos = [screenWidth / 2 - startButtonWidth / 2, current_startY]
        quitbtn.pos = [screenWidth / 2 - startButtonWidth / 2, current_startY + buttonHeight + spacing]

        # Falls "Custom" aktiv ist, zeichne das Eingabefeld
        display.fill(consts.BACKGROUND_COLOR)
        display.blit(title_surface, (screenWidth / 2 - title_surface.get_width() / 2, title_y))
        display.blit(instr_surface, (screenWidth / 2 - instr_surface.get_width() / 2, instr_y))
        player.draw()
        gameType.draw()
        timeLimit.draw()
        # Zeichne KI-Auswahl, falls nötig
        if gameType.getValue() == "human_ai":
            opponent_button_width = 150
            opponent_group_left = screenWidth / 2 - (opponent_button_width * 3 + spacing * 2) / 2
            opponent_group_top = timeLimitY + buttonHeight + spacing
            if aiSelection is None:
                aiSelection = ButtonGroup(
                    top=opponent_group_top,
                    left=opponent_group_left,
                    buttonList=[
                        Button(display=display, w=opponent_button_width, h=buttonHeight,
                               text="Minimax", value="minimax",
                               bgColor=consts.THM_COLOR,
                               selectedBgColor=consts.WHITE,
                               textColor=consts.BLACK),
                        Button(display=display, w=opponent_button_width, h=buttonHeight,
                               text="MCTS", value="mcts",
                               bgColor=consts.THM_COLOR,
                               selectedBgColor=consts.WHITE,
                               textColor=consts.BLACK),
                        Button(display=display, w=opponent_button_width, h=buttonHeight,
                               text="Random", value="random",
                               bgColor=consts.THM_COLOR,
                               selectedBgColor=consts.WHITE,
                               textColor=consts.BLACK)
                    ],
                    selected=0
                )
            else:
                aiSelection.top = opponent_group_top
                aiSelection.left = opponent_group_left
            aiSelection.draw()
        start.draw(12, 12, 12, 12)
        quitbtn.draw(12, 12, 12, 12)
        # Zeige Custom-Time Eingabefeld, falls aktiv
        if timeLimit.getValue() == "custom":
            input_box = pygame.Rect(screenWidth / 2 - 50, custom_input_y, 100, 40)
            pygame.draw.rect(display, consts.WHITE, input_box, 2)
            font_input = pygame.font.SysFont('arial', 30)
            input_surface = font_input.render(custom_input_text, True, consts.WHITE)
            display.blit(input_surface, (input_box.x + 5, input_box.y + 5))
            hint = font_input.render("mm:ss or mm", True, consts.WHITE)
            display.blit(hint, (screenWidth / 2 - hint.get_width() / 2, input_box.y - 30))
        game.drawTHMLogo()
        if error_message:
            font_error = pygame.font.SysFont('arial', 25)
            error_surface = font_error.render(error_message, True, (255, 0, 0))
            display.blit(error_surface, (screenWidth / 2 - error_surface.get_width() / 2, screenHeight - 50))
        pygame.display.update()
