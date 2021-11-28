###################################################################
#       Imported Files
from board import *
# 112_graphs, random, card, bid,
# special_bid, helper button imported via board
from bot import *
###################################################################

class Game():

    def __init__(self, app, playerDict):
        self.boardNumber = 1
        self.board = Board(self.boardNumber, app)
        self.ewPoints = 0
        self.nsPoints = 0
        self.players = playerDict # dict where key=position, value=Player
        self.history = [] # list of previous boards
        self.getBotPosition() # self.botPosition as a str

    # creates new board, stores old board, and increases board number
    def newBoard(self, app):
        self.history.append(self.board)
        self.boardNumber += 1
        self.board = Board(self.boardNumber, app)
        # keep settings consitent across board
        self.board.cardSkin = self.history[-1].cardSkin
        




    # assigns a str of botPositions to self.botPosition
    def getBotPosition(self):
        self.botPosition = '' 
        for position in self.players:
            if isinstance(self.players[position], Bot):
                self.botPosition += position

    # draws players usernames below their cards
    def drawUsernames(self, canvas, positionDict, activePosition):
        sampleCard = Card(14, 'S') # created arbitrary card to get height value (so changes are consistent + no magic no.)
        length = self.board.cardDislayWidth * 12 + sampleCard.width # width of initial hand
        height = sampleCard.height//3 # height of username display box
        for position in positionDict:
            color =  ['light grey', 'yellow'][int(position == activePosition)]
            x, y = positionDict[position]
            bottomEdge = y + sampleCard.height//2
            create_roundedRectangles(canvas,
                                    x - length//2, bottomEdge - height, 
                                    x + length//2, bottomEdge, 
                                    fill=color)
        #TODO add usernames

    # returns True is the game has ended
    def isGameEnd(self):
        return (self.board.drawBoardNumber > 34)

    # draws the game over screen
    def drawGameOver(self):
        pass
        
