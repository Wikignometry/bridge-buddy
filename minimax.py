###################################################################
#       Imported Modules
from node import *
from heuristic import *
###################################################################
#

# maximizing player is ns player regardless of who the bot is playing as
def minimax(node, depth, alpha, beta, isNSPlayer, heuristic):
    if node.hands[node.activePosition] == [] or depth == 0:
        return heuristic(node) 
    elif isNSPlayer:
        value = float('-inf')
        for key in node.children:
            child = node.children[key]
            value = max(value, minimax(child, depth-1, alpha, beta, False))
    else:
        value = float('inf')
        for key in node.children:
            child = node.children[key]
            value = min(value, minimax(child, depth-1, alpha, beta, True))
    return value 




