# file containing the buttons in the settings
from button import *

def getSettingsButtons():
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
def locateSettingsButtons(app, x, y):
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


