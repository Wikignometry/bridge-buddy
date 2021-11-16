# class of node for the minimax function
###################################################################
#       Imported Modules/Files
import copy
from board import *
# 112_graphs, random, card, bid,
# special_bid, helper button imported via board
from heuristic import *
###################################################################
#

class Node(Board):

    def __init__(self, hands, activePosition, currentRound, nsTricks, ewTricks, bid):
        self.hands = hands # dict represented by key=position and value=list of Cards
        self.activePosition = activePosition # n, s, e or w

        # dict key=str(card) and 
        self.children = self.getChildren() 

        self.currentRound = currentRound # is None if its the initial node, else is Card that was played to get to this position

        self.ewTricks = ewTricks # int (0-13)
        self.nsTricks = nsTricks # int (0-13)

        self.lead = self.currentRound[0][1] # Card

        self.bid = bid

        self.minimax = None # int value of the minimax heuristic value of the node

    # returns a list child Nodes from this node
    def getChildren(self):
        children = dict() # key=str(Card), value=Node
        for card in self.hands[self.activePosition]:

            childHands = copy.deepcopy(self.hands) # Cards are aliased, but we shouldn't be changing any of its attributes
            childHands[self.activePosition].remove(card) #removes card from hand
            
            # in normal circumstance where round has not ended
            if len(self.currentRound) < 4:
                childActivePosition, childCurrentRound, childTricks = self.continueRound(card)
            # when four cards have been played in the round
            else: 
                childActivePosition, childCurrentRound, childTricks = self.endRound(card)
            childNSTricks, childEWTricks = childTricks
            # creates a dict of all the children in the hand
            children[str(card)] = Node(childHands, 
                                        childActivePosition, childCurrentRound,
                                        childNSTricks, childEWTricks)

        return children
    
    # returns the child's activePosition and currentRound if the round continues
    def continueRound(self, card):
        childCurrentRound = self.currentRound + [(self.activePosition, card)]
        return ('nesw'[('nesw'.index(self.activePosition)+1)%4], 
                childCurrentRound, 
                (self.nsTricks, self.ewTricks))

    # returns the child's activePosition and currentRound if the round ends
    def endRound(self, card):
        # getWinner requires self.lead and self.bid
        winner, _ = self.getWinner(self.currentRound) # returns winning position and winning card (because recursion)
        if winner in 'ew': 
            childEWTricks = self.ewTricks + 1
        else: 
            childNSTricks = self.nsTricks + 1
        return (winner, 
                [(self.activePosition, card)], 
                (childNSTricks, childEWTricks))
        #   childActivePosition, childCurrentRound

    # calculates new minimax values from given depth for node and its children
    # takes in a heuristic function
    def calculateMinimax(self, depth, isNSPlayer, heuristic):
        if self.hands[self.activePosition] == [] or depth == 0:
            self.minimax = heuristic(self) 
        elif isNSPlayer:
            value = float('-inf')
            for key in self.children:
                childNode = self.children[key]
                value = max(value, childNode.calculateMinimax(depth-1, False))
            self.minimax = value
        else:
            value = float('inf')
            for key in self.children:
                childNode = self.children[key]
                value = min(value, childNode.calculateMinimax(depth-1, False))
            self.minimax = value
        return self.minimax    

###################################################################
#       Test Functions


