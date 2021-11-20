# mode for the menu screen
###################################################################
#       Imported Files

from mode_game import *
# 112_graphs, random, card, bid, heuristic, copy
# special_bid, helper button, node, game, bot, player imported via mode_game

###################################################################

# def initiateMenu(app):
def appStarted(app):
    app.mode = 'menuMode'
    app.buttons = [
        Button((400, 150), location=(app.width//2, app.height//2),
                 label = 'Play Solo', action=initiateGameMode, 
                 fill='deep sky blue', fontSize = 30, textFill='black', r=40)
    ]

def menuMode_mousePressed(app, event):
    soloPlayers = {
        'n': Player('Player1'),
        'e': Bot('e', 4, 9),
        's': Bot('s', 4, 9),
        'w': Bot('w', 4, 9),
    }
    for button in app.buttons:
        if button.isPressed(event.x, event.y): 
            button.action(app, soloPlayers)

def menuMode_redrawAll(app, canvas):
    for button in app.buttons:
        button.draw(canvas)


runApp(width=1200, height=700)