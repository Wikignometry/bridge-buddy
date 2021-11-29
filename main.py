###################################################################
#       Imported Modules

import math
import pygame
###################################################################
#       Imported Files

from mode_menu import *
# 112_graphs, random, card, bid, heuristic, copy, mode_game
# special_bid, helper button, node, game, bot, player imported via mode_menu
from sound import *
###################################################################

def appStarted(app):
    initiateMenu(app)
    app.mode = 'menuMode'
    pygame.mixer.init()
    app.sounds = {
        'button': Sound('media/button_click.wav'),
        'card': Sound('media/play_card.wav')
    } # dict of key=sound label and value=Sound

        



runApp(width=1200, height=700)
