# mode for the splashscreen
###################################################################
#       Imported Files
from mode_menu import *
# 112_graphs, random, card, bid, heuristic, copy, mode_game, 
# special_bid, helper button, node, game, bot, player imported via mode_menu
from cmu_112_graphics import *
from card import *
###################################################################

def initiateSplash(app):
    app.mode = 'splashMode'
    app.displayCard = [Card(14,'S'), Card(5,'H'), Card(14,'D'), Card(14,'C'), Card(2,'C')]
    locateDisplayCards(app)
    app.hoveredCard = None
    
# locates the display cards
def locateDisplayCards(app):
    # x0, y0 references the top left of the card
    displayWidth = 50
    splitWidth = 300
    xCard = app.width//2 - (displayWidth*((len(app.displayCard))//2)) - splitWidth//2 #leftmost center
    yCard = app.height//2 - app.height//10
    for card in app.displayCard:
        card.location = (xCard, yCard)
        xCard += displayWidth
        if card == Card(5,'H'):
            xCard += splitWidth
        card.fontSize = 16
        card.width, card.height = card.width*1.5, card.height*1.5


def splashMode_keyPressed(app, event):
    initiateMenu(app)

def splashMode_mouseMoved(app, event):
    print('moved')
    for card in app.displayCard:
        if card.isPressed(event.x, event.y): # not pressed, only hovered, but same idea
            print('foo')
            app.hoveredCard = card
            return
    app.hoveredCard = None
    locateDisplayCards(app)
    
#FIXME!!! Why doesn't this work?
def splashMode_mouseMoved(app, event):
    if app.hoveredCard != None:
        app.hoveredCard.move(0.3)          

def splashMode_redrawAll(app, canvas):
    # draws cards
    for card in app.displayCard:
        card.draw(canvas)

    # draws grey rectangle
    canvas.create_rectangle
    width, height = 2*app.width//3, app.height//5
    x0, y0 = (app.width - width)//2, (app.height - height)//2 # top left corner
    create_roundedRectangles(canvas, x0, y0, x0+width, y0+height, fill='light grey')    
    
    canvas.create_text(app.width//2, app.height//2,
                        text='Bridge Buddy',
                        anchor='center', font=('Ubuntu', 80, 'bold'), fill='black')
    canvas.create_text(app.width//2, app.height - 20, anchor = 's',
                        text='Press any key to start', font=('Ubuntu', 20, 'bold'))



