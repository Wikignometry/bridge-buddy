###################################################################
#       Imported Files
from card import *
# 112_graphs, draw_helpers and button imported via card
###################################################################


class Board():

    def __init__(self, boardNumber):
        
        # int – index (starts at 0) because it's easier to use
        self.index = boardNumber - 1

        self.dealer = 'nesw'[self.boardIndex % 4] # 'n','e','s' or 'w'
        self.vul = self.getVulnerability() # '', 'ns', 'ew', 'nsew'

        self.bids = [] # list of tuples(position, Bid)


    # returns str of vulnerable pair(s)
    def getVulnerability(self):
        vulnerabilities = ['', 'ns', 'ew', 'nsew']
        return vulnerabilities[(self.index//4 + self.index) % 4]