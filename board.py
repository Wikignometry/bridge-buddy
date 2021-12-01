###################################################################
#       Imported Files
from card import *
from bid import *
# 112_graphs, helper and button imported via card/bid
import random
from special_bid import *
###################################################################

class Board():

    def __init__(self, boardNumber, app):
        
        # int – index (starts at 0) because it's easier to use
        self.index = boardNumber - 1

        self.dealer = 'nesw'[self.index % 4] # 'n','e','s' or 'w'
        self.vul = self.getVulnerability() # '', 'ns', 'ew', 'nsew'

        self.bids = [] # list of tuples(position, Bid)
        self.bidOptions = self.getAllBids() # 2D list of all eligible bids
        self.bid = None # will become a Bid
        self.declarer = None # will become 'n','e','s' or 'w' after bidding end

        self.status = 'b' # 'b' (bidding) or 'p' (playing)
        
        self.endBoard = False # turns to true when board ends

        self.cardSkin = 'full' #light or full
        self.loadImages(app)

        self.dealHand() #self.hands = dict(key=position, value=list of Cards)
        self.sortHands()
        self.currentRound = [] #list of tuples (position, bid)
        self.lead = None # Card of first card in each round

        self.activePosition = self.dealer # 'n','e','s', 'w' or None

        self.cardDislayWidth = 30 # width of the card shown when in hand format

        self.ewTricks = 0 # int
        self.nsTricks = 0 # int
        # tracks what cards have already been played
        self.history = [] # list of tuples of each round

        self.endBoard = False # turns to True when the board is over (animation checks for this)


    # returns str of vulnerable pair(s)
    def getVulnerability(self):
        vulnerabilities = ['', 'ns', 'ew', 'nsew']
        return vulnerabilities[(self.index//4 + self.index) % 4]

    # deals cards to each hand (note to future Fa: this could really easily be repurposed for other card games)
    def dealHand(self):
        hands = dict()
        cardsPerPlayer = 13 # so its not magic
        allCards = makeDeck() # imported from helper
        for direction in 'nesw':
            hands[direction] = []
            for _ in range(cardsPerPlayer):
                dealtCard = random.choice(allCards) 
                allCards.remove(dealtCard) # prevents the card from being dealt twice
                hands[direction].append(dealtCard)
        self.hands = hands

    # sort the hands into the right order
    def sortHands(self):
        for position in 'nsew':
          self.hands[position].sort()

    # returns a list of all possible bids (excluding special ones)
    def getAllBids(self):
        bidOptions = []
        for contract in range(1,8):
            bidOptionsRow = []
            for trump in ['C', 'D', 'H', 'S', 'NT']:
                bidOptionsRow.append(Bid(contract, trump))
            bidOptions.append(bidOptionsRow)
        bidOptions.append([SpecialBid('Pass'), SpecialBid('X'), SpecialBid('XX')])
        return bidOptions

    # assigns the location of the bids based on a center of the grid
    def locateBids(self, location):
        xCenter, yCenter = location # refers to center of bidding grid
        # x, y is the top left of the bid grid
        x = xCenter + (40 * 2) # 40 is the width of button + 10, 2 is the # of bids between center and end
        y = yCenter - (40 * 2) + 15 # like above except 15 is the distance to the center of the bid
        for row in self.bidOptions: 
            for bid in row[::-1]:
                bid.location = (x, y)
                x -= 35
            x = xCenter + (40 * 2)
            y += 22
        for bid in self.bidOptions[-1]:
            bid.locate((xCenter, yCenter))

    # completes actions that need to happend when a bid is clicked
    def playBid(self, bid):
        if not self.isValidBid(bid): # invalid bids are changed to passes
            bid = SpecialBid('Pass')
        if isinstance(bid, Bid): # specialBids have superclass Button, not Bid
            self.clearLowerBids(bid)
        self.bids.append((self.activePosition, copy.deepcopy(bid))) # to prevent aliasing mania
        self.activePosition = 'nesw'[('nesw'.index(self.activePosition)+1)%4]

    # returns False is bid is not a bidOption
    def isValidBid(self, bid):
        for row in self.bidOptions:
            for bidOption in row:
                if bidOption == bid:
                    return True
        return False


    # completes the actions required to end bidding
    def endBidding(self):
        self.bid = SpecialBid('Pass') # sets in case it is a passout
        for position, bid in self.bids[::-1]: 
            if not isinstance(bid, SpecialBid): # so doubles and redoubles are not counted
                self.bid = bid
                self.declarer = position
                break
        if self.bid == SpecialBid('Pass'):
            print('endBoard')
            self.endBoard = True 
        self.status = 'p'
        self.activePosition = 'nesw'[('nesw'.index(self.activePosition)+1)%4]
        # to skip the dealer and lead from their left

    # returns True if the bidding has ended
    def isBiddingEnd(self):
        if len(self.bids) < 4:
            return False
        else:
            for _, bid in self.bids[-3:]:
                if bid != SpecialBid('Pass'): 
                    return False
            return True

    # removes all the bids in bidOptions lower than the bid given
    def clearLowerBids(self, bid):
        clearedRows = []
        while bid not in self.bidOptions[0]: # clears the rows
            self.bidOptions.pop(0)
            clearedRows.append([])
        while bid != self.bidOptions[0][0]: # clears the columns
            self.bidOptions[0].pop(0)
        self.bidOptions[0].pop(0) # to remove the bid itself
        self.bidOptions = clearedRows + self.bidOptions

    # draws all the available bids 
    def drawPotentialBids(self, canvas):
        for row in self.bidOptions:
            for bid in row[::-1]:
                if bid != None:
                    bid.draw(canvas)

    # actions to perform when a card is pressed
    def playCard(self, card, targetLocation):
        
        card.flipped = False

        # first card played is the lead
        if self.currentRound == []:
            self.lead = card

        self.hands[self.activePosition].remove(card)
        self.currentRound.append((self.activePosition, card))
        card.targetLocation = targetLocation

        # moves active position in a clockwise direction
        self.activePosition = 'nesw'[('nesw'.index(self.activePosition)+1)%4]
        
        # check for a round ending
        if len(self.currentRound) >= 4:
            self.endRound()
        
    # returns True if play is legal
    def isLegalPlay(self, card):
        if self.lead == None: return True
        return (self.lead.suit == card.suit or 
            not self.lead.containsSuit(self.hands[self.activePosition]))


    # location is a tuple (x, y) of the center of the hand
    def locateHand(self, hand, location):
        xCenter, yCenter = location
        cardCount = len(hand)
        x = xCenter - (self.cardDislayWidth*(cardCount//2)) #leftmost center
        y = yCenter
        for card in hand:
            card.location = (x, y)
            x += self.cardDislayWidth

    # locateHand for all four positions
    def locateHands(self, positionDict):
        for position in 'nsew':
            self.locateHand(self.hands[position], positionDict[position])

    # flip given hand 
    def flipHand(self, hand):
        for card in hand:
            card.flipped = not card.flipped 

    # performs all the neccesary actions for a round end
    def endRound(self):
        winner, _ = self.getWinner(self.currentRound) # returns winning position and winning card (because recursion)
        self.history.append(tuple(self.currentRound)) # make into a tuple to ensure it doesn't change
        self.currentRound = []
        self.activePosition = winner
        if winner in 'ew':
            self.ewTricks += 1
        else: self.nsTricks += 1

        self.lead = None # clears self.lead so isLegalPlay works

    # takes in list of tuple (position, card) 
    # returns the winnerPosition, winningCard in a round recursively 
    def getWinner(self, cardList):
        if len(cardList) == 1:
            return cardList[0]
        else:
            bestOfTheRest = self.getWinner(cardList[1:])
            # isGreaterThanInGame takes into account lead and trumps which are not taken into account by < or >
            if cardList[0][1].isGreaterThanInGame(bestOfTheRest[1], self.bid, self.lead):
                return cardList[0]
            else: 
                return bestOfTheRest

    # loads the card images
    def loadImages(self, app):
        fullImage = app.loadImage('media/cards.png')
        self.cardImages = dict()
        for row in range(5):
            suit = 'CDHSe'[row] #clubs, diamonds, heart, spades, else
            for col in range(13):
                card = fullImage.crop((col*157, row*229, (col+1)*157+3, (row+1)*228+3))
                card = app.scaleImage(card, 2/5)
                # sets the image to a dictionary where key=Card
                if suit != 'e':
                    self.cardImages[Card((col+12)%13+2, suit)] = card
                elif suit == 'e' and col == 2:
                    self.cardImages['back'] = card
        

    # draw each card in the hand
    def drawHands(self, canvas):
        for position in 'nsew':
            for card in self.hands[position]:
                if self.cardSkin == 'light':
                    card.draw(canvas)
                elif self.cardSkin == 'full':
                    if card.flipped == False:
                        canvas.create_image(card.location[0], card.location[1], image=ImageTk.PhotoImage(self.cardImages[card]))
                    else:
                        canvas.create_image(card.location[0], card.location[1], image=ImageTk.PhotoImage(self.cardImages['back']))

    # draw played cards in the current round
    def drawPlayedCards(self, canvas):
        for _ , card in self.currentRound: 
            if self.cardSkin == 'light':
                    card.draw(canvas)
            elif self.cardSkin == 'full':
                if card.flipped == False:
                        canvas.create_image(card.location[0], card.location[1], image=ImageTk.PhotoImage(self.cardImages[card]))
                else:
                    canvas.create_image(card.location[0], card.location[1], image=ImageTk.PhotoImage(self.cardImages['back']))


    # draws the bidding history 
    def drawBidHistory(self, app, canvas):
        width = app.width//4
        height = app.height//3
        x1, y1 = (app.width, app.height) # refers to bottom right of the screen
        create_roundedRectangles(canvas, 
                                x1 - width, y1 - height,
                                x1, y1, outline=None,
                                fill = 'light grey')
        xCenter, yCenter = x1 - width//2, y1 - height//2
        self.drawBidColumns(canvas, xCenter, yCenter, width, height)

    # draws the columns for the bids to be in and the bids themselves
    def drawBidColumns(self, canvas, xCenter, yCenter, width, height):
        colWidth = width//6
        colHeight = 5*height//7
        margin = 10
        # x0, y0 is the top right of the area with bid columns
        x0, y0 = xCenter - colWidth*2 - margin*1.5, yCenter - colHeight//2 + height//15
        for i in range(4):
            xCol, yCol = x0+i*(colWidth+margin), y0 # top left of each col
            canvas.create_text(xCol + colWidth//2, yCol - 10, 
                                anchor='s', text='NESW'[i],
                                font=('Calbri', 16, 'bold'))
            create_roundedRectangles(canvas, 
                                    xCol, yCol,
                                    xCol+colWidth, yCol+colHeight,
                                    fill='dark grey', outline=None)
            for ii in range(len(self.bids)):
                position, bid = self.bids[ii] 
                if position == 'nesw'[i]: # if position is the column we are drawing
                    bid.location = (xCol + colWidth//2, yCol + (ii//4)*22 + bid.height//2 + margin) 
                    # 22 based on the arbitrary number used for the bidding grid
                    bid.draw(canvas)


    # draw statistics 
    def drawStatistics(self, app, canvas):
        width = app.width//4
        height = app.height//5
        create_roundedRectangles(canvas, 0, app.height - height, 
                                width, app.height, fill='black')
        leftEdge = self.drawBoardBox(app, canvas, height) # box that indicated board no., dealer, and vulnerabilities
        leftEdge = self.drawTricks(app, canvas, height, leftEdge)
        if self.status == 'p':
            self.drawFinalBid(app, canvas, leftEdge)

    # draws a larger final bid in the stats box
    def drawFinalBid(self, app, canvas, leftEdge):
        contract = copy.deepcopy(self.bid)
        contract.width, contract.height = (60, 54)
        contract.fontSize = 25
        contract.location = (leftEdge + contract.width//2 + 5, app.height - 10 - contract.height//2)
        contract.draw(canvas)

    # draw an indication of number of trick gained for each pair
    def drawTricks(self, app, canvas, boxHeight, leftEdge):
        margin = 10
        height = (boxHeight - 3*margin)//2
        width = 80
        create_roundedRectangles(canvas, leftEdge + margin, app.height - margin - height, 
                                    leftEdge + margin + width, app.height - margin,
                                    fill='light grey')
        canvas.create_text(leftEdge + margin + width//2, app.height - margin - height//2,
                                text=f'ns: {self.nsTricks}', font=('Calbri', 20))
        create_roundedRectangles(canvas, leftEdge + margin, app.height - 2*(margin + height), 
                                    leftEdge + margin + width, app.height - (2*margin + height),
                                    fill='light grey')
        canvas.create_text(leftEdge + margin + width//2, app.height - 2*(margin + height) + height//2,
                                text=f'ew: {self.ewTricks}', font=('Calbri', 20))
        return leftEdge + 15 + width
        


    # draw boardBox (see competitive analysis)
    def drawBoardBox(self, app, canvas, statBoxHeight):
        width = statBoxHeight - 20
        rightEdge = 10 + width # places box on left edge of stats board
        # rightEdge = statBoxWidth - 10 # places box on right edge of stats box
        bottomEdge = app.height - 10

        # draws box and corresponding red/white triangles (shows as trapezoids)
        self.drawVulnerabilities(canvas, rightEdge, bottomEdge, width)
        
        # draws the board number and the square that encapsulates it
        self.drawBoardNumber(canvas, rightEdge, bottomEdge, width)
        
        # draws the letter 'D' to indicate the dealer
        self.drawDealer(canvas, rightEdge, bottomEdge, width)
        return rightEdge
    
    # draws the D for who the dealer is
    def drawDealer(self, canvas, rightEdge, bottomEdge, width):
        # dict relating dealer position to where each of the 'D' should go
        positionDict = {'n': (rightEdge - width//2, bottomEdge - 9*width//10),
                        'e': (rightEdge - width//10, bottomEdge - width//2),
                        's': (rightEdge - width//2, bottomEdge - width//10),
                        'w': (rightEdge - 9*width//10, bottomEdge - width//2)}
        x0, y0 = positionDict[self.dealer]
        canvas.create_text(x0, y0, text='D', font=('Calbri', '20', 'bold'))                

    # draws the board number in boardBox
    def drawBoardNumber(self, canvas, rightEdge, bottomEdge, width):
        canvas.create_rectangle(rightEdge - 4*width//5, bottomEdge - 4*width//5, 
                                rightEdge - width//5, bottomEdge - width//5, 
                                fill='light grey', outline='black')
        canvas.create_text(rightEdge - width//2, bottomEdge - width//2, 
                            text=self.index + 1, font=('Calbri', '40'))


    # draws the rectangle/triangles for the vulnerabilities 
    def drawVulnerabilities(self, canvas, rightEdge, bottomEdge, width):
        
        # create the square (show ew vulnerabilitieis)
        ewVulColor = ['white', 'firebrick3'][int('ew' in self.vul)]
        canvas.create_rectangle( 
                                rightEdge - width, bottomEdge - width, 
                                rightEdge, bottomEdge, 
                                fill=ewVulColor, outline='black')
        
        # create the shape to display vulnerabilities for NS
        nsVulColor = ['white', 'firebrick3'][int('ns' in self.vul)]
        canvas.create_polygon(rightEdge - width, bottomEdge - width, 
                              rightEdge, bottomEdge - width,
                              rightEdge - width//2, bottomEdge - width//2,
                              fill=nsVulColor, outline='black')
        canvas.create_polygon(rightEdge - width, bottomEdge, 
                              rightEdge, bottomEdge,
                              rightEdge - width//2, bottomEdge - width//2,
                              fill=nsVulColor, outline='black')


###################################################################
#           Helper Function

# make a deck of 52 cards
def makeDeck():
    fullDeck = list()
    for suit in 'SHDC': 
        for number in range(2, 15): # ace is treated as 14
            fullDeck.append(Card(number, suit))
    return fullDeck

###################################################################
#       Test Functions

# returns True if there are duplicates (used to test duplicates in deck/hand)
def hasDuplicates(L):
    strList = list(map(str, L)) # reprs all the objects
    return (list(set(strList)) == strList)


def testBoardClass():
    print('Testing Board...', end='')
    board1 = Board(17)
    assert(board1.vul == '')
    board2 = Board(4)
    assert(board2.vul == 'nsew')
    assert(board1.dealer == 'n')
    assert(len(board1.hands['n']) == 13)
    assert(Bid(5,'C') in board1.bidOptions[4])
    assert(Bid(6,'NT') in board1.bidOptions[5])
    assert(Bid(1,'S') in board1.bidOptions[0])
    assert(Bid(4,'D') in board1.bidOptions[3])
    assert(not hasDuplicates(makeDeck()))
    for position in 'nsew':
        assert(not hasDuplicates(board1.hands[position]))
    board1.lead = Card(8,'H')
    board1.bid = Bid(4,'S')
    board1.bids = [('n', Bid(1,'S')), ('e', Bid(2,'S')), ('w', SpecialBid('Pass')), ('s', SpecialBid('Pass')), ('n', SpecialBid('Pass'))]
    assert(board1.getWinner([('n', Card(8,'H')), ('s', Card(2,'S')), ('e', Card(7,'D')), ('w', Card(3,'S'))]) == ('w', Card(3,'S'))) 
    assert(board1.getWinner([('s', Card(8,'H')), ('e', Card(9,'H')), ('w', Card(11,'H')), ('n', Card(13,'D'))])== ('w', Card(11,'H')))    
    assert(board1.isBiddingEnd() == True)
    board1.bids = [('n', Bid(1,'S')), ('e', Bid(2,'S')), ('w', SpecialBid('Pass')), ('s', SpecialBid('Pass'))]
    assert(board1.isBiddingEnd() == False)
    board1.bids = [('w', SpecialBid('Pass')), ('s', SpecialBid('Pass')), ('n', SpecialBid('Pass'))]
    assert(board1.isBiddingEnd() == False)
    print('Passed!')

# def appStarted(app):
#     app.board1 = Board(15)
#     app.board1.bid = Bid(4,'S') # bid is currently hard coded. 
#     app.board1.locateBids((app.width//2, app.height//2)) 
# def mousePressed(app, event):
#     if app.board1.status == 'p':
#         # checks if card is pressed and does corresponding actions
#         for card in (app.board1.hands[app.board1.activePosition])[::-1]:
#             if card.isPressed(event.x, event.y):
#                 app.board1.playCard(card, (app.width//2, app.height//2))
#                 return
#     # checks if bid is pressed and does corresponding actions
#     if app.board1.status == 'b':
#         for row in app.board1.bidOptions:
#             for bid in row:
#                 if bid.isPressed(event.x, event.y):
#                     app.board1.playBid(bid)
#     print(app.board1.bids)


# def timerFired(app):
#     for _ , card in app.board1.currentRound:
#         card.move(0.3)

# def redrawAll(app, canvas):
#     app.board1.locateHands({'n': (app.width//2, 50), 
#                             'e': (app.width-250, app.height//2), 
#                             's': (app.width//2, app.height-50), 
#                             'w': (250, app.height//2)})
#     app.board1.drawHands(canvas)
#     app.board1.drawPlayedCards(canvas)
#     if app.board1.status == 'b':
#         app.board1.drawPotentialBids(canvas)

# test cropping the cards
# def appStarted(app):
#     app.board = Board(1)
#     app.board.loadImages(app)
#     app.handLocations = {'n': (app.width//2, 50),
#                             'e': (app.width-250, app.height//2), 
#                             's': (app.width//2, app.height-50), 
#                             'w': (250, app.height//2)}
#     app.board.locateHands(app.handLocations)

# def redrawAll(app, canvas):
#     app.board.drawHands(canvas)

###################################################################
#       Code to run

# testBoardClass()
# runApp(width=1200, height=700)
