# class of node for the minimax function
###################################################################
#       Imported Modules
import copy

###################################################################
#

class Node():

    def __init__(self, hands, activePosition, currentRound, cardPlayed=None):
        self.hands = hands # class Board
        self.activePosition = activePosition # n, s, e or w
        self.children = self.getChildren() # list of child nodes
        self.cardPlayed = cardPlayed # is None if its the initial node, else is Card that was played to get to this position

    # returns a list child Nodes from this node
    def getChildren(self):
        children = []
        for card in self.hands[self.activePosition]:
            childHands = copy.deepcopy(self.hands)
            childHands[self.activePosition].remove(card) #removes card from hand
            nextActivePosition = self.getNextPosition()
            children.append(Node(childHands, nextActivePosition, card))
        return children
    
    #FIXME
    def getNextPosition(self):
        if 
    