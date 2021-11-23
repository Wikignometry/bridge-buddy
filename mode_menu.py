# mode for the menu screen
###################################################################
#       Imported Files

from mode_game import *
# 112_graphs, random, card, bid, heuristic, copy
# special_bid, helper button, node, game, bot, player imported via mode_game

###################################################################

def getMenuPlayersDict():
    solo = {
        'n': Player('PlayerNorth'),
        'e': Bot('e', 4, 9),
        's': Bot('s', 4, 9),
        'w': Bot('w', 4, 9),
    }
    teaching = {
        'n': Player('PlayerNorth'),
        'e': Player('PlayerEast'),
        's': Player('PlayerSouth'),
        'w': Player('PlayerWest'),
    }

    return {
        'Play Solo': solo,
        'Teaching\nMode': teaching
    }


# def initiateMenu(app):
def appStarted(app):
    app.mode = 'menuMode'
    app.buttons = [
        Button((app.width//4, app.height//5), location=(app.width//3, app.height//2),
                 label = 'Play Solo', action=initiateGameMode, 
                 fill='deep sky blue', fontSize = 30, textFill='black', r=40),
        Button((app.width//8, app.height//5), location=(app.width//3 + app.width//5, app.height//2),
                label = 'Teaching\nMode', action=initiateGameMode, 
                fill='lime green', fontSize = 30, textFill='black', r=40)
    ]
    app.menuPlayersDict = getMenuPlayersDict() # dict where key=button name and value=playersDict

def menuMode_mousePressed(app, event):
    
    for button in app.buttons:
        if button.isPressed(event.x, event.y): 
            button.action(app, app.menuPlayersDict[button.label])

def menuMode_redrawAll(app, canvas):
    for button in app.buttons:
        button.draw(canvas)


runApp(width=1200, height=700)

