###################################################################
#       Imported Files
from card import *
from bid import *
# 112_graphs, draw_helpers and button imported via card/bid
import random
from helper import *
from special_button import *
###################################################################

class Board():

    def __init__(self, boardNumber):
        
        # int – index (starts at 0) because it's easier to use
        self.index = boardNumber - 1

        self.dealer = 'nesw'[self.index % 4] # 'n','e','s' or 'w'
        self.vul = self.getVulnerability() # '', 'ns', 'ew', 'nsew'

        self.bids = [] # list of tuples(position, Bid)
        self.bidOptions = self.getAllBids() # 2D list of all eligible bids
        self.bid = None

        self.status = 'b' # 'b' (bidding) or 'p' (playing)
        
#TODO: implement bidding system

        #TODO: remove harcoding
        self.hands = {'n': [Card(3,'D'), Card(14,'S'), Card(7,'S'), Card(6,'S'), Card(14,'D'), Card(9,'C'), Card(13,'H'), Card(5,'C'), Card(13,'S'), Card(8,'H'), Card(8,'C'), Card(3,'H'), Card(7,'H')], 'e': [Card(2,'D'), Card(11,'D'), Card(9,'D'), Card(6,'C'), Card(8,'C'), Card(6,'H'), Card(3,'S'), Card(5,'S'), Card(5,'H'), Card(7,'D'), Card(4,'C'), Card(6,'D'), Card(4,'H')], 's': [Card(4,'D'), Card(12,'S'), Card(13,'D'), Card(4,'S'), Card(10,'S'), Card(11,'H'), Card(9,'S'), Card(11,'S'), Card(10,'D'), Card(13,'C'), Card(14,'C'), Card(2,'C'), Card(3,'C')], 'w': [Card(12,'C'), Card(12,'H'), Card(2,'H'), Card(12,'D'), Card(14,'H'), Card(7,'C'), Card(8,'D'), Card(9,'H'), Card(10,'C'), Card(11,'C'), Card(2,'S'), Card(10,'H'), Card(5,'D')]}
        # self.dealHand() #self.hands = dict(key=position, value=list of Cards)
        self.sortHands()
        self.currentRound = [] #list starting with leading position, then contains all the cards played in clockwise direction
        self.lead = None # Card of first card in each round

        #TODO: remember to remove hardcoding
        self.activePosition = 'n' # 'n','e','s', 'w' or None

        self.cardDislayWidth = 30 # width of the card shown when in hand format

        self.ewTricks = 0 # int
        self.nsTricks = 0 # int
        # tracks what cards have already been played
        self.history = [] # list of tuples of each round

    # returns str of vulnerable pair(s)
    def getVulnerability(self):
        vulnerabilities = ['', 'ns', 'ew', 'nsew']
        return vulnerabilities[(self.index//4 + self.index) % 4]

    # deals cards to each hand (note to future Fa: this could really easily be repurposed for other card games)
    def dealHand(self):
        hands = dict()
        cardsPerPlayer = 13
        allCards = self.makeDeck()
        for direction in 'nesw':
            hands[direction] = []
            for _ in range(cardsPerPlayer):
                dealtCard = random.choice(allCards) 
                allCards.remove(dealtCard) # prevents the card from being dealt twice
                hands[direction].append(dealtCard)
        self.hands = hands

    # make a deck of 52 cards
    def makeDeck(self):
        fullDeck = list()
        for suit in 'SHDC': 
            for number in range(2, 15): # ace is treated as 14
                fullDeck.append(Card(number, suit))
        return fullDeck

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
        bidOptions.append([SpecialBid('Pass')])
        return bidOptions

    # assigns the location of the bids based on a center of the grid
    def locateBids(self, location):
        xCenter, yCenter = location # refers to center of bidding grid
        # x, y is the top left of the bid grid
        x = xCenter - (40 * 2) # 40 is the width of button + 10, 2 is the # of bids between center and end
        y = yCenter - (40 * 2) - 15 # like above except 15 is the distance to the center of the bid
        for row in self.bidOptions[:-1]: 
            for bid in row:
                bid.location = (x, y)
                x += 35
            x = xCenter - (40 * 2)
            y += 22
        self.bidOptions[-1][0].locate((xCenter, yCenter))

    # completes actions that need to happend when a bid is clicked
    def playBid(self, bid):
        if isinstance(bid, Bid):
            self.clearLowerBids(bid)
        self.bids.append((self.activePosition, bid))
        self.activePosition = 'nesw'[('nesw'.index(self.activePosition)+1)%4]
        if self.isBiddingEnd():
            print('foo')
            self.endBidding()
    
    # completes the actions required to end bidding
    def endBidding(self):
        index = 1
        while self.bids[-index][1] == 'Pass':
            index += 1
        self.bid = self.bids[-index][1]
        self.status = 'p'


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
        while bid not in self.bidOptions[0]: # clears the rows
            self.bidOptions.pop(0)
        while bid != self.bidOptions[0][0]: # clears the columns
            self.bidOptions[0].pop(0)
        self.bidOptions[0].pop(0) # to remove the bid itself

    # draws all the available bids 
    def drawPotentialBids(self, canvas):
        for row in self.bidOptions:
            for bid in row[::-1]:
                if bid != None:
                    bid.draw(canvas)

    # actions to perform when a card is pressed
    def playCard(self, card, targetLocation):
        self.hands[self.activePosition].remove(card)
        self.currentRound.append((self.activePosition, card))
        card.targetLocation = targetLocation
        # moves active position in a clockwise direction
        self.activePosition = 'nesw'[('nesw'.index(self.activePosition)+1)%4]
        # checks for round end
        if len(self.currentRound) >= 4:
                self.endRound()

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

    # performs all the neccesary actions for a round end
    def endRound(self):
        self.lead = self.currentRound[0][1] #TODO: this might have to move somewhere more efficient
        winner, _ = self.getWinner(self.currentRound) # returns winning position and winning card (because recursion)
        self.history.append(tuple(self.currentRound)) # make into a tuple to ensure it doesn't change
        self.currentRound = []
        self.activePosition = winner
        if winner in 'ew':
            self.ewTricks += 1
        else: self.nsTricks += 1

    # returns the winner in a round recursively
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

    # draw each card in the hand
    def drawHands(self, canvas):
        for position in 'nsew':
            for card in self.hands[position]:
                card.draw(canvas)

    # draw played cards in the current round
    def drawPlayedCards(self, canvas):
        for _ , card in self.currentRound: 
            card.draw(canvas)

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
    assert(not hasDuplicates(board1.makeDeck()))
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

def appStarted(app):
    app.board1 = Board(15)
    app.board1.bid = Bid(4,'S') # bid is currently hard coded. #TODO: remove hardcoding
    app.board1.locateBids((app.width//2, app.height//2)) #TODO: locate bids again if screen resizes

def mousePressed(app, event):
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
    print(app.board1.bids)


def timerFired(app):
    for _ , card in app.board1.currentRound:
        card.move(0.3)

def redrawAll(app, canvas):
    app.board1.locateHands({'n': (app.width//2, 50), 
                            'e': (app.width-250, app.height//2), 
                            's': (app.width//2, app.height-50), 
                            'w': (250, app.height//2)})
    app.board1.drawHands(canvas)
    app.board1.drawPlayedCards(canvas)
    if app.board1.status == 'b':
        app.board1.drawPotentialBids(canvas)

###################################################################
#       Code to run

testBoardClass()
runApp(width=1200, height=700)
