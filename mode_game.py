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
    try:
        app.mode = 'gameMode'

        app.timeElapsed = 0 
        app.delay = 500

        app.error = False

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
        
        if app.teaching == False:
            for position in 'nsew':
                if app.game.players[position] != app.player:
                    app.board.flipHand(app.board.hands[position])
        
        app.board.locateBids((app.width//2, app.height//2))
        app.board.locateHands(app.handLocations)
        for position in app.game.botPosition:
            player = app.game.players[position]
            player.interpretInitialHand(app.board.hands[position])
        
        
        
        print(f'app.connection: {app.connection} ')
        if app.connection == 'server': # server is north
            server(app)
            app.partner = app.game.players['s'] # south is hardcoded as the socket
            app.partner.acceptSocket(app) 
            app.partner.sendSeed()
        elif app.connection == 'client':
            client(app)
            app.player.createSocket(app) 
            app.player.getSeed()
            print('client!')
    except:
        app.error = True
        return

def gameMode_mousePressed(app, event):   
    try:
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
                        
                            # so the active position is right
                            # if it is the client's turn and you're the client
                            if app.board.activePosition == 's' and app.connection == 'client':
                                print('client sendingBidinMode')
                                app.player.sendBid(bid) # send the bid to the server
                            # if it is the server's turn and you're the server
                            elif app.board.activePosition == 'n' and app.connection == 'server':
                                print('server sendingBidinMode')
                                app.partner.sendBid(bid) # send the bid to your partner
                        


                            app.board.playBid(bid)
                            
                            # plays sound effects
                            if app.soundEffects:
                                app.sounds['button'].start()
                            
                            # checks for end of bidding
                            if app.board.isBiddingEnd():
                                endBidding(app)

                            app.timeElapsed = 0 # so timer starts after last play

                        

        ##################### playing #####################
        if app.board.status == 'p': # when cardplay is occuring
            # loop in reverse order so cards the topmost card is activated when pressed
            for card in (app.board.hands[app.board.activePosition])[::-1]:
                if card.isPressed(event.x, event.y) and app.board.isLegalPlay(card):

                    # sockets
                        # if it is the client's turn and you're the client
                        if app.board.activePosition == 's' and app.connection == 'client':
                            app.player.sendCard(card) # send the card to the server
                        # if it is the server's turn and you're the server
                        elif app.board.activePosition == 'n' and app.connection == 'server':
                            app.partner.sendCard(card) # send the card to your partner


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
    except Exception as e:
        app.error = True
        print(e)


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
    if app.soundEffects:
        app.sounds['card'].start()

# repositions items when size of screen changes
def gameMode_sizeChanged(app):
    app.board.locateBids((app.width//2, app.height//2))
    app.handLocations = {'n': (app.width//2, 50),
                            'e': (app.width-250, app.height//2), 
                            's': (app.width//2, app.height-50), 
                            'w': (250, app.height//2)}
    app.board.locateHands(app.handLocations)

def gameMode_keyPressed(app, event):
    if app.error:
        app.error = False
        app.game = None
        for button in app.buttons:
            if button.label == 'menu':
                button.action(app) # return to menu screen

def gameMode_timerFired(app):
    try:
        app.timeElapsed += app.timerDelay

        for _ , card in app.board.currentRound:
            card.move(0.3) #TODO: fix magic number?
        
        if app.board.index >= 33: # there are 34 boards in a tournament in Bridge
            app.game = None # end game
            for button in app.buttons:
                if button.label == 'menu':
                    button.action(app) # return to menu screen


        ##################### bots #####################
        if isinstance(app.game.players[app.board.activePosition], Bot) and app.timeElapsed >= app.delay:
            app.timeElapsed = 0
            if app.board.status == 'p':
                botPlay(app) 
            else:
                botBid(app)
            return # so bots and sockets are separate

        ##################### sockets #####################
        # if it is the client's turn and you're the server
        if app.timeElapsed <= app.delay: return # to create a delay between card play
        elif app.board.activePosition == 's' and app.connection == 'server':
            if app.board.status == 'b':
                print('server gettingBid in mode')
                bid = app.partner.getBid() # get bid from partner
                app.board.playBid(bid)
                if app.board.isBiddingEnd():
                    endBidding(app)

                # plays sound effects
                if app.soundEffects:
                    app.sounds['button'].start()

            if app.board.status == 'p':
                card = app.partner.getCard() # get bid from partner
                for cardInHand in app.board.hands[app.board.activePosition]:
                    if cardInHand == card:
                        card = cardInHand # so the images attributes etc. are kept
                app.board.playCard(card, app.playedCardPositions[app.board.activePosition])

                # card sounds effect
                if app.soundEffects:
                    app.sounds['card'].start()
        
        # if it is the server's turn and you're the client
        if app.board.activePosition == 'n' and app.connection == 'client':
            
            if app.board.status == 'b':
                print('client gettingBid in mode')
                bid = app.player.getBid() # get bid from partner
                app.board.playBid(bid)
                if app.board.isBiddingEnd():
                    endBidding(app)

                # plays sound effects
                if app.soundEffects:
                    app.sounds['button'].start()
                print('gotBid')

            if app.board.status == 'p':
                card = app.player.getCard() # get bid from partner
                for cardInHand in app.board.hands[app.board.activePosition]:
                    if cardInHand == card:
                        card = cardInHand # so the images attributes etc. are kept
                app.board.playCard(card, app.playedCardPositions[app.board.activePosition])

                # card sounds effect
                if app.soundEffects:
                    app.sounds['card'].start()
            return
    except Exception as e:
        app.error = True
        print(e)





def gameMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='#2C6337') 
    app.board.drawHands(canvas) 
    app.board.drawPlayedCards(canvas)
    if app.board.status == 'b':
        app.board.drawPotentialBids(canvas)
    app.board.drawStatistics(app, canvas)
    app.game.drawUsernames(canvas, app.handLocations, app.board.activePosition)
    app.board.drawBidHistory(app, canvas)
    for button in app.buttons:
        button.draw(canvas)
    if app.error:
        drawError(app,canvas) #TODO

def drawError(app, canvas):
    create_roundedRectangles(canvas, app.width//4, 2*app.height//5, 3*app.width//4, 3*app.height//5, fill='#a7d1ca') 
    canvas.create_text(app.width//2, app.height//2, anchor = 'center', justify='center',
                        text='Error...\nPress any key to return to menu', font=('Ubuntu', 36, 'bold'))




###################################################################
#       Code to run

# runApp(width=1200, height=700)
