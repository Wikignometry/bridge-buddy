###################################################################
#       Imported Modules
from node import *
###################################################################
#

def minimax(node, depth, alpha, beta, isMaxPlayer):
    if node.hands[node.activePosition] == [] or depth == 0:
        return heuristic(node) # TODO: heuristic function
    elif isMaxPlayer:
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


