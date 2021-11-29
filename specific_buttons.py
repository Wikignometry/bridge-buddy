# file containing the buttons in the settings
###################################################################
#       Imported Files
from button import *
from mode_menu import *
# 112_graphs, random, card, bid, heuristic, copy, mode_game
# special_bid, helper button, node, game, bot, player imported via mode_menu
###################################################################




# returns the top level buttons already located
def getTopLevelButtons(app):
    margin = 10
    width, height = 100, 40
    return [
        Button(
            (width, height), # dimensions
            action=initiateMenu,
            fill='light grey',
            label='menu', location=(margin + width//2, margin + height//2)
            ),
        Button(
            (width, height), # dimensions
            action=toggleSetting,
            fill='light grey',
            label='settings', location=(app.width-margin - width//2, margin + height//2)
            )
    ]

# adds or remove setting Buttons
def toggleSetting(app, _):
    settingButtons = getSettingButtons()
    locateSettingButtons
    if settingButtons in app.buttons:
        app.buttons.append(settingButtons)
    else:
        removeButtons(app, settingButtons)

def removeButtons(app, buttonList):
    for button in app.buttons:
        if button in buttonList:
            app.buttons.remove(button)


def getSettingButtons():
    settingButtons = []
    settingButtonsDict = { # each function takes in app and button
        'card skin: full': changeCardSkin,
        'music: none': changeMusic,
        'sound effects: on': toggleSoundEffects,
        'cheating ai: off': toggleCheating,
    }
    for label in settingButtonsDict:
        settingButtons.append(
            Button(
            (120, 80), # dimensions
            action=settingButtonsDict[label],
            fill='light grey'
            )
        )
    return settingButtons

# takes in x, y of the center of the lower edge of the settings
def locateSettingButtons(app, x, y):
    margin = 10
    for i in range(len(app.settingButtons)):
        button = app.settingButtons[i]
        button.location = (x, y + button.height + margin)


# changes the card skin and labels between given options 
def changeCardSkin(app, button):
    app.board.cardSkin = ['light', 'full'][int(app.board.cardSkin == 'light')]
    button.label = f'card skin: {app.board.cardSkin}'

# changes background music
def changeMusic(app, button):
    musicList = ['none', 'nature', 'piano']
    app.music = musicList[musicList.index(app.music)-1] 
    button.label = f'music: {app.music}'
    #rotates is reverse because list indexing can deal with negatives, but not out of bounds

# turns on/off sound effects
def toggleSoundEffects(app, button):
    #toggles between True and False
    app.soundEffects = not app.soundEffects
    labelText = ['off', 'on'][int(app.soundEffects)]
    button.label = f'sound effects: {labelText}'

def toggleCheating(app, button):
    for position in app.game.botPosition:
        app.game.players[position].cheater = not app.game.players[position].cheater
    labelText = ['off', 'on'][int(app.game.players['n'].cheater)]
    button.label = f'cheating ai: {labelText}'


