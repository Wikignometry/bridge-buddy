###################################################################
#       Imported Files
from board import *
# 112_graphs, random, card, bid,
# special_bid, helper button imported via board
###################################################################

class Game():

    def __init__(self, playerDict):
        self.boardNumber = 1
        self.board = Board(self.boardNumber)
        self.ewPoints = 0
        self.nsPoints = 0
        self.players = playerDict # dict where key=position, value=Player
        self.history = [] # list of previous boards

    def newBoard(self):
        self.history.append(self.board)
        self.boardNumber += 1
        self.board = Board(self.boardNumber)
