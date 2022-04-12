# mode for the menu screen
###################################################################
#       Imported Files

from mode_game import *
# 112_graphs, random, card, bid, heuristic, copy
# special_bid, helper button, node, game, bot, player imported via mode_game

###################################################################

def getMenuPlayersDict(app):
    solo = {
        'n': app.player,
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

    partner = {
        'n': app.player,
        'e': Bot('e', 4, 9),
        's': Player('client'),
        'w': Bot('w', 4, 9),
    }

    joinPartner = {
        'n': Player('server'),
        'e': Bot('e', 4, 9),
        's': app.player,
        'w': Bot('w', 4, 9),
    }


    return {
        'Play solo': solo,
        'Teaching\nMode': teaching,
        'Join\nPartner': joinPartner,
        'Play with a partner': partner
    }

# color scheme from https://coolors.co/185d9e-00a5cf-4dcae3-25a18e-7ae582-25b7fa
def initiateMenu(app, *args): # args so polymorphism works
    app.mode = 'menuMode'
    margin = 10

    if app.connection != None and app.player.socket != None:
            app.player.sendMessage('') # so the partner knows you have left the game
            app.player.socket = None
    
    app.connection = None # so it clears after a connected game
    app.teaching = False # ditto

    xCenter, yCenter = app.width//2, app.height//2
    buttonWidth, buttonHeight = app.width//5, 2*app.height//7 # refers to width of small button
    yTopRow = yCenter - margin//2 - buttonHeight//2
    yBottomRow = yCenter + margin//2 + buttonHeight//2
    xDifferenceLarge = buttonWidth//2 # distance from centerline for large buttons
    xDifferenceSmall = buttonWidth + margin # distance from centerline for small buttons
    app.menuButtons = [
        Button((2*buttonWidth, buttonHeight), location=(xCenter-xDifferenceLarge, yTopRow),
                 label = 'Play solo', action=initiateGameMode, 
                 fill='#23C491', fontSize = 30, textFill='black', textAnchor='se', font='Ubuntu', r=40, style='bold', 
                 overlay='media/image1.jpg', overlayAlpha=100, overlayLocation=(-20, 0), overlayScale=0.7),
        
        Button((buttonWidth, buttonHeight), location=(xCenter+xDifferenceSmall, yTopRow),
                label = 'Teaching\nMode', action=initiateGameMode, font='Ubuntu', style='bold',
                fill='#25A18E', fontSize = 30, textFill='white', r=40),
        
        Button((2*buttonWidth, buttonHeight), location=(xCenter+xDifferenceLarge, yBottomRow),
                label = 'Play with a partner', action=initiateGameMode, 
                fill='#4DCAE3', fontSize = 30, textFill='black', textAnchor='se', r=40,
                font='Ubuntu', style='bold', 
                overlay='media/image5.jpg', overlayAlpha=90, overlayScale=1),
        
        Button((buttonWidth, buttonHeight), location=(xCenter-xDifferenceSmall, yBottomRow),
                label = 'Join\nPartner', action=initiateGameMode, font='Ubuntu', style='bold',
                fill='#00A5CF', fontSize = 30, textFill='white', r=40)
    ]
    app.menuPlayersDict = getMenuPlayersDict(app) # dict where key=button name and value=playersDict
    

def menuMode_mousePressed(app, event):
    # persistent buttons
    for button in app.buttons:
        if button.isPressed(event.x, event.y):
            
            # plays sound effect if enabled (before screen change)
            if app.soundEffects:
                app.sounds['button'].start()

            button.action(app, button)
    
    # menu buttons
    for button in app.menuButtons:
        if button.isPressed(event.x, event.y): 

            #play sound effect if enabled (before screen change)
            if app.soundEffects:
                app.sounds['button'].start()

            if button.label == 'Join\nPartner':
                app.connection = 'client'
            elif button.label == 'Play with a partner':
                app.connection = 'server'
            elif button.label == 'Teaching\nMode':
                app.teaching = True
            button.action(app, app.menuPlayersDict[button.label])
            


def menuMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#1F4447')
    for button in app.menuButtons:
        button.draw(canvas)
    for button in app.buttons:
        button.draw(canvas)

    # canvas.create_image(2*app.width//3, app.height//2-app.height//10, image=ImageTk.PhotoImage(app.overlay))



