# mode for the bridge game
###################################################################
#       Imported Files

from node import *
# 112_graphs, random, card, bid, heuristic, copy
# special_bid, helper button imported via node
from game import *
from bot import *
# player imported via bot
###################################################################

def appStarted(app):
    app.mode = 'gameMode'
    app.game = Game({'n': Player('Fa'), 
                    's': Bot('s', 4, 9), 
                    'e': Player('Fa'), 
                    'w': Player('Fa')})
    app.board = app.game.board
    print(app.game.botPosition)
    app.board.locateBids((app.width//2, app.height//2))
    app.playedCardPositions = {
                                'n': (app.width//2, app.height//2 - 57), # 57 is width of a card
                                'e': (app.width//2 + 57, app.height//2),
                                's': (app.width//2, app.height//2 + 57),
                                'w': (app.width//2 - 57, app.height//2)
    }


def gameMode_mousePressed(app, event):
    # checks if bid is pressed and does corresponding actions
    if app.board.status == 'b':
        for row in app.board.bidOptions:
            for bid in row:
                if bid.isPressed(event.x, event.y):
                    app.board.playBid(bid)
                    if app.board.isBiddingEnd():
                        app.board.endBidding()
                        # assigns the bid and hand in the bot
                        for botPosition in app.game.botPosition:
                            app.game.players[botPosition].startPlay(app.board.hands[botPosition])
                            app.game.players[botPosition].assignBid(app.board.bid)
    if app.board.status == 'p':
        # checks if card is pressed and does corresponding actions
        for card in (app.board.hands[app.board.activePosition])[::-1]:
            if card.isPressed(event.x, event.y):
                app.board.playCard(card, app.playedCardPositions[app.board.activePosition])
                # checks for round end
                
                print(f'currentRound: {app.board.currentRound}')
                while isinstance(app.game.players[app.board.activePosition], Bot):
                    print(app.game.players[app.board.activePosition], app.board.activePosition)
                    botPlay(app) #FIXME make it have a delay - move to timerFired?
                break
    if app.board.endBoard:
        app.game.newBoard()
        app.board = app.game.board 
        app.board.locateBids((app.width//2, app.height//2))
    # adjusts the card position for played card
    app.board.locateHands({'n': (app.width//2, 50),
                            'e': (app.width-250, app.height//2), 
                            's': (app.width//2, app.height-50), 
                            'w': (250, app.height//2)})

# function for when the bot is playing
def botPlay(app):
    # app.game.players[app.board.activePosition].makeNode(app.board.hands, 4, app.board.activePosition, app.board.currentRound, 0, 0, app.board.bid)
    chosenCard = app.game.players[app.board.activePosition].playTurn(app.board.currentRound, app.board.nsTricks, app.board.ewTricks)
    print(f'botPlay: {chosenCard, app.board.activePosition}')

    app.board.playCard(chosenCard, app.playedCardPositions[app.board.activePosition])

# repositions items when size of screen changes
def gameMode_sizeChanged(app):
    app.board.locateBids((app.width//2, app.height//2))
    app.board.locateHands({'n': (app.width//2, 50),
                            'e': (app.width-250, app.height//2), 
                            's': (app.width//2, app.height-50), 
                            'w': (250, app.height//2)})

def gameMode_timerFired(app):
    for _ , card in app.board.currentRound:
        card.move(0.3) #TODO: fix magic number?

def gameMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='forest green') 
    app.board.drawHands(canvas) 
    app.board.drawPlayedCards(canvas)
    if app.board.status == 'b':
        app.board.drawPotentialBids(canvas)
    app.board.drawStatistics(app, canvas)



###################################################################
#       Code to run

runApp(width=1200, height=700)
