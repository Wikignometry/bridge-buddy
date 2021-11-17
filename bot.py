# bot class
###################################################################
#       Imported Files
from player import *
from helper import *
from node import *
# 112_graphs, random, card, bid, board, copy
# special_bid, helper button, heuristic imported via node
###################################################################


class Bot():

    def __init__(self):
        self.history = []
        # self.possibleNodes = [] # list of Nodes
        # self.hand = None # list of Cards in the bot's hand

    def makeNode(self, hands, depth, activePosition, currentRound, nsTricks, ewTricks, bid):
        self.node = Node(hands, depth, activePosition, currentRound, nsTricks, ewTricks, bid)

    def botTurn(self):
        self.node.calculateMinimax(True, baseHeuristic)
        return self.node.getPlay()


    # def startBoard(self, hand):
    #     self.hand = hand
    
    # def playTurn(self):
    #     self.generateMonteCarloHands()

    # # prunes Monte Carlo when a card becomes available    
    # def updateMonteCarlo(self, position, card):
    #     for i in range(len(self.possibleNodes)):
    #         if card in self.possibleNodes[i].hands[position]:
    #             self.possibleNodes[i] = self.possibleNodes[i].children[str(card)]
    #         else:
    #             self.possibleNodes.pop(i)
    #             self.generateMonteCarlo # appends new node to 
            
    
    # def generateMonteCarlo(self):
    #     montyHand = dict()
    #     montyHand[self.position] = self.hand

    #     pass

    # # returns a deck with all the cards that we have not 
    # def makeUnkownDeck(self):

    
