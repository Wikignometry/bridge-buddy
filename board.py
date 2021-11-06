###################################################################
#       Imported Files
from card import *
from bid import *
# 112_graphs, draw_helpers and button imported via card/bid
import random
###################################################################


class Board():

    def __init__(self, boardNumber):
        
        # int – index (starts at 0) because it's easier to use
        self.index = boardNumber - 1

        self.dealer = 'nesw'[self.index % 4] # 'n','e','s' or 'w'
        self.vul = self.getVulnerability() # '', 'ns', 'ew', 'nsew'

        self.bids = [] # list of tuples(position, Bid)
        self.bidOptions = self.getAllBids()

        self.dealHand() #self.hands = dict(key=position, value=list of Cards)

    #returns a list of all possible bids (excluding special ones)
    def getAllBids(self):
        bidOptions = []
        for contract in range(1,7):
            for trump in ['C', 'D', 'H', 'S', 'NT']:
                bidOptions.append(Bid(contract, trump))
        return bidOptions

    # returns str of vulnerable pair(s)
    def getVulnerability(self):
        vulnerabilities = ['', 'ns', 'ew', 'nsew']
        return vulnerabilities[(self.index//4 + self.index) % 4]

    # deals 13 cards to each hand
    def dealHand(self):
        hands = dict()
        cardsPerPlayer = 13
        allCards = self.makeDeck()
        for direction in 'nesw':
            hands[direction] = []
            for _ in range(cardsPerPlayer):
                hands[direction].append(random.choice(allCards))
        hands['played'] = []
        self.hands = hands

    # make a deck of 52 cards
    def makeDeck(self):
        fullDeck = list()
        for suit in 'SHDC': 
            for number in range(2, 15): # ace is treated as 14
                fullDeck.append(Card(number, suit))
        return fullDeck

###################################################################
#       Test Functions

def testBoardClass():
    print('Testing Board...', end='')
    board1 = Board(17)
    assert(board1.vul == '')
    assert(board1.dealer == 'n')
    assert(len(board1.hands['n']) == 13)
    print(board1.bidOptions)
    assert(Bid(5,'C') in board1.bidOptions)
    assert(Bid(6,'NT') in board1.bidOptions)
    assert(Bid(1,'S') in board1.bidOptions)
    assert(Bid(4,'D') in board1.bidOptions)
    print('Passed!')


###################################################################
#       Code to run

testBoardClass()

