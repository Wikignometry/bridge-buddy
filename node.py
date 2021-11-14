# class of node for the minimax function
###################################################################
#       Imported Modules
import copy
from board import *
###################################################################
#

class Node(Board):

    def __init__(self, hands, activePosition, currentRound, ewTricks, nsTricks):
        self.hands = hands # dict represented by key=position and value=list of Cards
        self.activePosition = activePosition # n, s, e or w
        self.children = self.getChildren() # list of child nodes
        self.currentRound = currentRound # is None if its the initial node, else is Card that was played to get to this position

        self.ewTricks = ewTricks # int (0-13)
        self.nsTricks = nsTricks # int (0-13)

        self.lead = self.currentRound[0][1] # Card

    # returns a list child Nodes from this node
    def getChildren(self):
        children = dict() # key=str(Card), value=Node
        for card in self.hands[self.activePosition]:

            childHands = copy.deepcopy(self.hands) # Cards are aliased, but we shouldn't be changing any of its attributes
            childHands[self.activePosition].remove(card) #removes card from hand
            
            # in normal circumstance where round has not ended
            if len(self.currentRound) < 4:
                childActivePosition, childCurrentRound = self.continueRound(card)
            # when four cards have been played in the round
            else: 
                childActivePosition, childCurrentRound = self.endRound(card)
            children[str(card)] = Node(childHands, 
                                        childActivePosition, childCurrentRound,
                                        self.ewTricks, self.nsTricks)

        return children
    
    # returns the child's activePosition and currentRound if the round continues
    def continueRound(self, card):
        childCurrentRound = self.currentRound + [(self.activePosition, card)]
        return 'nesw'[('nesw'.index(self.activePosition)+1)%4], childCurrentRound

    # returns the child's activePosition and currentRound if the round ends
    def endRound(self, card):
        winner, _ = self.getWinner(self.currentRound) # returns winning position and winning card (because recursion)
        if winner in 'ew':
            self.ewTricks += 1
        else: self.nsTricks += 1
        return winner, [(self.activePosition, card)]
        #   childActivePosition, childCurrentRound
