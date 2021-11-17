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

    def __init__(self, hands, depth, activePosition, currentRound, nsTricks, ewTricks, bid):
        self.depth = depth # int of how deep the node goes
        self.hands = hands # dict represented by key=position and value=list of Cards
        self.activePosition = activePosition # n, s, e or w

        self.currentRound = currentRound # list of tuples (position, card)

        self.ewTricks = ewTricks # int (0-13)
        self.nsTricks = nsTricks # int (0-13)

        self.lead = self.currentRound[0][1] # Card

        self.bid = bid

        # dict key=str(card) and 
        self.children = self.getChildren() 

        self.minimax = None # int value of the minimax heuristic value of the node

    # returns a list child Nodes from this node
    def getChildren(self):
        children = dict() # key=str(Card), value=Node
        for card in self.hands[self.activePosition]:

            childHands = copy.deepcopy(self.hands) # Cards are aliased, but we shouldn't be changing any of its attributes
            childHands[self.activePosition].remove(card) #removes card from hand
            
            # in normal circumstance where round has not ended
            if len(self.currentRound) < 4:
                if not self.islegalPlay(card): continue
                childActivePosition, childCurrentRound, childTricks = self.continueRound(card)
            # when four cards have been played in the round
            else: 
                childActivePosition, childCurrentRound, childTricks = self.endRound(card)
            childNSTricks, childEWTricks = childTricks
            # creates a dict of all the children in the hand
            children[str(card)] = Node(childHands, self.depth-1,
                                        childActivePosition, childCurrentRound,
                                        childNSTricks, childEWTricks, self.bid
                                        )

        return children
    
    # returns True if play is legal
    def islegalPlay(self, card):
        lead = self.currentRound[0][1] # the first card in the round
        return (lead.suit == card.suit or 
            not lead.containsSuit(self.hands[self.activePosition]))

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
        childEWTricks, childNSTricks = self.ewTricks, self.nsTricks
        if winner in 'ew': 
            childEWTricks += 1
        else: 
            childNSTricks += 1
        return (winner, 
                [(self.activePosition, card)], 
                (childNSTricks, childEWTricks))
        #   childActivePosition, childCurrentRound

    # calculates new minimax values from given depth for node and its children
    # takes in a heuristic function
    # inspired by pseudocode from https://en.wikipedia.org/wiki/Minimax
    def calculateMinimax(self, isNSPlayer, heuristic):
        if self.hands[self.activePosition] == [] or self.depth == 0:
            self.minimax = heuristic(self) 
        elif isNSPlayer:
            value = float('-inf')
            for key in self.children:
                childNode = self.children[key]
                value = max(value, childNode.calculateMinimax(False, baseHeuristic))
            self.minimax = value
        else:
            value = float('inf')
            for key in self.children:
                childNode = self.children[key]
                value = min(value, childNode.calculateMinimax(False, baseHeuristic))
            self.minimax = value
        return self.minimax    

    def getPlay(self):
        if self.activePosition in 'ns': #maximizing player
            value = float('-inf')
            for key in self.children:
                if self.children[key].minimax > value:
                    value = self.children[key].minimax
                    cardStr = key
        else: # minimizing player
            value = float('inf')
            for key in self.children:
                if self.children[key].minimax < value:
                    value = self.children[key].minimax
                    cardStr = key
        for card in self.hands[self.activePosition]:
            if str(card) == cardStr:
                return card
        

###################################################################
#       Test Functions

def testNode():
    print('Testing Node...', end='')

