###################################################################
#       Imported Modules
from node import *
###################################################################

# super simple heuristic right now
def heuristic(node):
    # positive if ns gains more tricks than ew
    return node.nsTricks - node.ewTricks
