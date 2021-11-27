###################################################################
#       Imported Files
from node import *
###################################################################

# super simple heuristic right now
def baseHeuristic(node):
    # positive if ns gains more tricks than ew
    return node.nsTricks - node.ewTricks

# make this better




