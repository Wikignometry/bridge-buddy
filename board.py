###################################################################
#       Imported Files
from card import *
from bid import *
# 112_graphs, draw_helpers and button imported via card/bid
###################################################################


class Board():

    def __init__(self, boardNumber):
        
        # int – index (starts at 0) because it's easier to use
        self.index = boardNumber - 1

        self.dealer = 'nesw'[self.boardIndex % 4] # 'n','e','s' or 'w'
        self.vul = self.getVulnerability() # '', 'ns', 'ew', 'nsew'

        self.bids = [] # list of tuples(position, Bid)
        self.bidOptions = self.getAllBids()

    #returns a list of all possible bids (excluding special ones)
    def getAllBids():
        bidOptions = []
        for contract in range(1,7):
            for trump in ['C', 'D', 'H', 'S', 'NT']:
                bidOptions.append(Bid(contract, trump))
        return bidOptions

    # returns str of vulnerable pair(s)
    def getVulnerability(self):
        vulnerabilities = ['', 'ns', 'ew', 'nsew']
        return vulnerabilities[(self.index//4 + self.index) % 4]