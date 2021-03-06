###################################################################
#       Imported Modules

import pygame
###################################################################
#       Imported Files


# 112_graphs, random, card, bid, heuristic, copy, mode_game, mode_menu
# special_bid, helper button, node, game, bot, player imported via mode_splash
from sound import *
from mode_splash import *
from specific_buttons import * 
###################################################################

def appStarted(app):

    # splashscreen
    initiateSplash(app)

    # sound
    pygame.mixer.init()
    app.sounds = {
        'button': Sound('media/button_click.wav'),
        'card': Sound('media/play_card.wav'),
        'music': Music('media/music.mp3'),
        'nature': Music('media/nature.mp3'),
    } # dict of key=sound label and value=Sound

    # buttons
    app.buttons = getTopLevelButtons(app)

    # baseline
    app.game = None
    app.soundEffects = True
    app.music = app.sounds['music'] # 'music', 'nature' or 'off'
    app.connection = False # 'server' 'client' or False
    

def appStopped(app):
    if isinstance(app.music, Music):
        app.music.stop()



runApp(width=1200, height=700)
