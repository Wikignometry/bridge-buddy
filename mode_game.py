# mode for the bridge game
###################################################################
#       Imported Files

from node import *
# 112_graphs, random, card, bid, heuristic, copy
# special_bid, helper button imported via node
from game import *
from bot import *
# player imported via bot
from server import *
from client import *
###################################################################

# def appStarted(app):
def initiateGameMode(app, players):
    app.mode = 'gameMode'

    app.timeElapsed = 0 
    app.delay = 500

    if app.game == None or players != app.game.players:
        app.game = Game(app, players)
    app.board = app.game.board
    print(app.game.botPosition)
    app.handLocations = {'n': (app.width//2, 50),
                            'e': (app.width-250, app.height//2), 
                            's': (app.width//2, app.height-50), 
                            'w': (250, app.height//2)}
    app.playedCardPositions = {
                                'n': (app.width//2, app.height//2 - 57), # 57 is width of a card
                                'e': (app.width//2 + 57, app.height//2),
                                's': (app.width//2, app.height//2 + 57),
                                'w': (app.width//2 - 57, app.height//2)
    }
    app.board.locateBids((app.width//2, app.height//2))
    app.board.locateHands(app.handLocations)
    for position in app.game.botPosition:
        player = app.game.players[position]
        player.interpretInitialHand(app.board.hands[position])

    if app.connection == 'server': # server is north
        server(app)
        app.partner = app.game.players['s'] # south is hardcoded as the socket
        app.partner.acceptSocket(app) 
    elif app.connection == 'client':
        client(app)
        app.player.createSocket(app) 

def gameMode_mousePressed(app, event):
    ##################### buttons #####################
    for button in app.buttons:
        if button.isPressed(event.x, event.y):

            if app.soundEffects:
                app.sounds['button'].start()

            button.action(app, button)
    ##################### bidding #####################
    if app.board.status == 'b': 
         
        for row in app.board.bidOptions:
            for bid in row:

                if bid.isPressed(event.x, event.y):

                    app.board.playBid(bid)
                    
                    # plays sound effects
                    if app.soundEffects:
                        app.sounds['button'].start()
                    
                    # checks for end of bidding
                    if app.board.isBiddingEnd():
                        endBidding(app)

                    # if it is the client's turn and you're the client
                    if app.board.activePosition == 's' and app.connection == 'client':
                        app.player.sendBid(bid) # send the bid to the server
                    # if it is the server's turn and you're the server
                    elif app.board.activePosition == 'n' and app.connection == 'server':
                        app.partner.sendBid(bid) # send the bid to your partner
                    


                    app.timeElapsed = 0 # so timer starts after last play

    ##################### playing #####################
    if app.board.status == 'p': # when cardplay is occuring
        # loop in reverse order so cards the topmost card is activated when pressed
        for card in (app.board.hands[app.board.activePosition])[::-1]:
            if card.isPressed(event.x, event.y) and app.board.isLegalPlay(card):
                
                # plays sound effect if app.soundEffects is True
                if app.soundEffects: 
                    app.sounds['card'].start()

                app.board.playCard(card, app.playedCardPositions[app.board.activePosition])
                print(f'currentRound: {app.board.currentRound}')

                # updates known cards for the bot players
                for botPosition in app.game.botPosition:
                    app.game.players[botPosition].updateKnownCards(app.board.activePosition, card)
                
                app.timeElapsed = 0 # so timer starts after last play

                break # to prevent multiple overlapping cards from being pressed
        
        
    
    ##################### ending #####################
    if app.board.endBoard:
        app.game.newBoard(app)
        app.board = app.game.board #TODO: maybe change all app.board to app.game.board
        app.board.locateBids((app.width//2, app.height//2))
    
    ##################### miscellaneous #####################
    # adjusts the card position for played card
    app.board.locateHands(app.handLocations)



def endBidding(app):
    app.board.endBidding()   
    # assigns the bid and hand in the bot
    for botPosition in app.game.botPosition:
        app.game.players[botPosition].startPlay(app.board.hands[botPosition])
        app.game.players[botPosition].assignBid(app.board.bid)

def botBid(app):
    chosenBid = app.game.players[app.board.activePosition].playBid(app.board.bids)
    app.board.playBid(chosenBid)
    print(f'bids: {app.board.bids}')
    app.sounds['button'].start()
    
    if app.board.isBiddingEnd():
        endBidding(app)
    
    # plays sound effects
    if app.soundEffects:
        app.sounds['button'].start()
    

# function for when the bot is playing
def botPlay(app):
    chosenCard = app.game.players[app.board.activePosition].playTurn(app.board.currentRound, app.board.nsTricks, app.board.ewTricks, app.board.hands)
    print(f'botPlay: {chosenCard, app.board.activePosition}')
    app.board.playCard(chosenCard, app.playedCardPositions[app.board.activePosition])
    
    # card sounds effect
    if app.soundEffect:
        app.sounds['card'].start()

# repositions items when size of screen changes
def gameMode_sizeChanged(app):
    app.board.locateBids((app.width//2, app.height//2))
    app.handLocations = {'n': (app.width//2, 50),
                            'e': (app.width-250, app.height//2), 
                            's': (app.width//2, app.height-50), 
                            'w': (250, app.height//2)}
    app.board.locateHands(app.handLocations)

def gameMode_timerFired(app):
    
    app.timeElapsed += app.timerDelay

    for _ , card in app.board.currentRound:
        card.move(0.3) #TODO: fix magic number?
    
    ##################### bots #####################
    if isinstance(app.game.players[app.board.activePosition], Bot) and app.timeElapsed >= app.delay:
        app.timeElapsed = 0
        if app.board.status == 'p':
            botPlay(app) 
        else:
            botBid(app)

    ##################### sockets #####################
    # if it is the client's turn and you're the server
    if app.board.activePosition == 's' and app.connection == 'server':
<<<<<<< Updated upstream
        app.player.getBid()
=======
        if app.board.status == 'b':
            bid = app.partner.getBid() # get bid from partner
            app.board.playBid(bid)
            if app.board.isBiddingEnd():
                endBidding(app)

            # plays sound effects
            if app.soundEffects:
                app.sounds['button'].start()

        if app.board.status == 'p':
            card = app.partner.getCard() # get bid from partner
            app.board.playCard(card, app.playedCardPositions[app.board.activePosition])

            # card sounds effect
            if app.soundEffect:
                app.sounds['card'].start()
    
    # if it is the server's turn and you're the client
    if app.board.activePosition == 'n' and app.connection == 'client':
        if app.board.status == 'b':
            bid = app.player.getBid() # get bid from partner
            app.board.playBid(bid)
            if app.board.isBiddingEnd():
                endBidding(app)

            # plays sound effects
            if app.soundEffects:
                app.sounds['button'].start()

        if app.board.status == 'p':
            card = app.player.getCard() # get bid from partner
            app.board.playCard(card, app.playedCardPositions[app.board.activePosition])

            # card sounds effect
            if app.soundEffect:
                app.sounds['card'].start()
    



>>>>>>> Stashed changes


def gameMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='forest green') 
    app.board.drawHands(canvas) 
    app.board.drawPlayedCards(canvas)
    if app.board.status == 'b':
        app.board.drawPotentialBids(canvas)
    app.board.drawStatistics(app, canvas)
    app.game.drawUsernames(canvas, app.handLocations, app.board.activePosition)
    app.board.drawBidHistory(app, canvas)
    for button in app.buttons:
        button.draw(canvas)



###################################################################
#       Code to run

# runApp(width=1200, height=700)
