###################################################################
#       Imported Files
from card import *
###################################################################


def baseHeuristic(node):
    # positive if ns gains more tricks than ew
    heuristic = node.nsTricks - node.ewTricks

    # counts sure winners
    if node.bid.trump != 'NT':
        number = 14
        highestTrump = Card(number, node.bid.trump)
        if highestTrump in node.hands['n'] and highestTrump in node.hands['s']:
            while highestTrump in node.hands['n'] and highestTrump in node.hands['s']:
                heuristic += 1
                number -= 1
                highestTrump = Card(number, node.bid.trump)
        else:
            while highestTrump in node.hands['e'] and highestTrump in node.hands['w']:
                heuristic -= 1
                number -= 1
                highestTrump = Card(number, node.bid.trump)
    return heuristic






