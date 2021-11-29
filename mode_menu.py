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

def initiateMenu(app, *args): # args so polymorphism works
    app.mode = 'menuMode'
    app.menuButtons = [
        Button((app.width//3, 2*app.height//7), location=(app.width//3, app.height//2),
                 label = 'Play Solo', action=initiateGameMode, 
                 fill='deep sky blue', fontSize = 30, textFill='black', r=40),
        Button((app.width//5, 2*app.height//7), location=(2*app.width//3, app.height//2),
                label = 'Teaching\nMode', action=initiateGameMode, 
                fill='lime green', fontSize = 30, textFill='black', r=40)
    ]
    app.menuPlayersDict = getMenuPlayersDict() # dict where key=button name and value=playersDict
    app.overlay = overlayImage('media/bridge_board.png')
    app.overlay = app.scaleImage(app.overlay, 1/4)
    # rotation from https://pythontic.com/image-processing/pillow/rotate
    app.overlay = app.overlay.rotate(120, expand = 1)


# putalpha from https://stackoverflow.com/questions/24731035/python-pil-0-5-opacity-transparency-alpha

def overlayImage(path):
    overlay = Image.open(path)
    # based on https://github.com/python-pillow/Pillow/issues/4687
    # makes the image more transparent without displaying already transparent pixels
    overlayCopy = overlay.copy()
    overlayCopy.putalpha(180)
    overlay.paste(overlayCopy, overlay)
    return overlay
    

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

            button.action(app, app.menuPlayersDict[button.label])
            


def menuMode_redrawAll(app, canvas):
    for button in app.menuButtons:
        button.draw(canvas)
    for button in app.buttons:
        button.draw(canvas)

    canvas.create_image(2*app.width//3, app.height//2-app.height//10, image=ImageTk.PhotoImage(app.overlay))




