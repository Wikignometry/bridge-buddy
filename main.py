###################################################################
#       Imported Modules

import math

###################################################################
#       Imported Files

from mode_menu import *
# 112_graphs, random, card, bid, heuristic, copy, mode_game
# special_bid, helper button, node, game, bot, player imported via mode_menu

###################################################################

def appStarted(app):
    initiateMenu(app)
    app.mode = 'menuMode'


runApp(width=1200, height=700)
