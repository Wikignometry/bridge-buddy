###################################################################
#       Imported Files
from board import *
# 112_graphs, random, card, bid,
# special_bid, helper button imported via board
###################################################################

class Game():

    def __init__(self):
        self.boardNumber = 1
        self.board = Board(self.boardNumber)


    def newBoard(self):
        self.boardNumber += 1
        self.board = Board(self.boardNumber)