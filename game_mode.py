# mode for the bridge game
###################################################################
#       Imported Files

from node import *
# 112_graphs, random, card, bid, heuristic, copy
# special_bid, helper button imported via node
###################################################################

def appStarted(app):
    app.board1 = Board(15)
    app.board1.locateBids((app.width//2, app.height//2)) #TODO: locate bids again if screen resizes

def gameMode_mousePressed(app, event):
    if app.board1.status == 'p':
        # checks if card is pressed and does corresponding actions
        for card in (app.board1.hands[app.board1.activePosition])[::-1]:
            if card.isPressed(event.x, event.y):
                app.board1.playCard(card, (app.width//2, app.height//2))
                return
    # checks if bid is pressed and does corresponding actions
    if app.board1.status == 'b':
        for row in app.board1.bidOptions:
            for bid in row:
                if bid.isPressed(event.x, event.y):
                    app.board1.playBid(bid)

def gameMode_timerFired(app):
    for _ , card in app.board1.currentRound:
        card.move(0.3)

def gameMode_redrawAll(app, canvas):
    app.board1.locateHands({'n': (app.width//2, 50), 
                            'e': (app.width-250, app.height//2), 
                            's': (app.width//2, app.height-50), 
                            'w': (250, app.height//2)})
    app.board1.drawHands(canvas)
    app.board1.drawPlayedCards(canvas)
    if app.board1.status == 'b':
        app.board1.drawPotentialBids(canvas)
