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
            label='menu', location=(margin + width//2, margin + height//2),
            fontSize = 16
            ),
        Button(
            (width, height), # dimensions
            action=toggleSetting,
            fill='light grey',
            label='settings', location=(app.width-margin - width//2, margin + height//2),
            fontSize = 16
            )
    ]

# adds or remove setting Buttons
def toggleSetting(app, _):
    settingButtons = getSettingButtons()
    locateSettingButtons(app.buttons[-1].location, settingButtons)
    if settingButtons[0] not in app.buttons:
        app.buttons.extend(settingButtons)
        
    else:
        removeButtons(app, settingButtons)

def removeButtons(app, buttonList):
    for button in buttonList:
        app.buttons.remove(button)


def getSettingButtons():
    settingButtons = []
    settingButtonsDict = { # each function takes in app and button
        'card skin: full': changeCardSkin,
        'music: music': changeMusic,
        'sound effects: on': toggleSoundEffects,
        'cheating ai: off': toggleCheating,
    }
    for tag in settingButtonsDict:
        settingButtons.append(
            Button(
            (100, 40), # dimensions
            label=tag,
            action=settingButtonsDict[tag],
            fill='light grey'
            )
        )
    return settingButtons

# takes in x, y of the center of the lower edge of the settings
def locateSettingButtons(location, buttons):
    x, y = location
    margin = 10
    for i in range(len(buttons)):
        button = buttons[i]
        button.location = (x, y + (button.height + margin)*(i+1))


# changes the card skin and labels between given options 
def changeCardSkin(app, button):
    app.board.cardSkin = ['light', 'full'][int(app.board.cardSkin == 'light')]
    button.label = f'card skin: {app.board.cardSkin}'

# changes background music
def changeMusic(app, button):
    
    musicList = ['off', 'nature', 'music']

    # get the label
    if app.music == 'off':
        label = musicList[musicList.index('off')-1]
    else:
        label = musicList[musicList.index(app.music.path[6:-4])-1]
    
    
    if label == 'off':
        app.music.stop()
        app.music = 'off'
    else:
        app.music = app.sounds[label]
        app.music.start(loops=-1)
    
    button.label = f'music: {label}'
    #rotates is reverse because list indexing can deal with negatives, but not out of bounds

# turns on/off sound effects
def toggleSoundEffects(app, button):
    #toggles between True and False
    app.soundEffects = not app.soundEffects
    labelText = ['off', 'on'][int(app.soundEffects)]
    button.label = f'sound effects: {labelText}'

def toggleCheating(app, button):
    if app.game == None or app.game.botPosition == '': return # checks for no bots/game
    for position in app.game.botPosition:
        app.game.players[position].cheater = not app.game.players[position].cheater
    labelText = ['off', 'on'][int(app.game.players[app.game.botPosition[0]].cheater)]
    button.label = f'cheating ai: {labelText}'


