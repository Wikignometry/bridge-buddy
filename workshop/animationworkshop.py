# this is an old file that I played around in 
###################################################################
#       Imported Modules

from cmu_112_graphics import *
import random
import math

###################################################################
#       Basic Helper Functions

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

###################################################################
#       Classes

class Card():

    def __init__(self, suit, number): #for now, maybe add values later
        self.suit = suit # 'C', 'D', 'H', or 'S'
        self.number = number # int
        self.location = None # represented as a tuple of center of the card
        self.cardWidth = 57
        self.cardHeight = 89
        # actual dimensions (in mm) according to 
        # http://greatbridgelinks.com/poker-size-cards-vs-bridge-size-cards/
        if self.suit in 'DH':
            self.color = 'red'
        else: self.color = 'black'
    
    def __repr__(self):
        if self.number < 11:
            return str(self.number) + self.suit
        return 'JQKA'[self.number % 11] + self.suit

class Board():

    def __init__(self, boardNumber):
        self.boardIndex = boardNumber - 1
        self.dealer = 'nesw'[self.boardIndex % 4] 
        self.vulnerability = self.getVulnerability()
        self.cardDisplay = 30 # how much width of the card is shown when is hand
        self.dealHand() # sets self.hand to dict of 1d list of cards (indexed by position)

    def getVulnerability(self):
        vulnerabilities = ['', 'ns', 'ew', 'nsew']
        return vulnerabilities[(self.boardIndex//4 + self.boardIndex)%4]

    def dealHand(self):
        hands = dict()
        cardsPerPlayer = 13
        allCards = self.makeDeck()
        for direction in 'nesw':
            hands[direction] = []
            for _ in range(cardsPerPlayer):
                hands[direction].append(random.choice(allCards))
        hands['played'] = []
        self.hands = hands

    def makeDeck(self):
        fullDeck = list()
        for suit in 'SHDC': 
            for number in range(2, 15): # ace is treated as 14
                fullDeck.append(Card(suit, number))
        return fullDeck

    def locateHands(self, locationDict):
        for position in 'nsew':
            hand = self.hands[position]
            xCenter, yCenter = locationDict[position]
            x = xCenter - (len(self.hands[position]) * self.cardDisplay)//2
            y = yCenter
            for card in hand:
                card.location = (x, y)
                print(x, y)
                x += self.cardDisplay 

class Player():

    def __init__(self, username):
        self.username = username
        self.profileImage = None
        self.bio = None

class Game():

    def __init__(self, playerDict, yourPosition):
        self.ewPoints = 0 #int
        self.nsPoints = 0 #int
        self.boardNumber = 1 #int
        self.board = Board(self.boardNumber) #Board (class)
        self.players = playerDict 
        # {'n':'player1', 'e':'player2', 's':'player3', 'w':'player4'}
        self.yourPosition = yourPosition #TODO: fix this
        # str ('n','s','e','w') who are you playing as
    
    def newBoard(self):
        self.boardNumber += 1
        self.board = Board(self.boardNumber)
        
###################################################################
#       Animations!!!!
###################################################################
#       Controllers 

# returns False if a card wasn't pressed, else returns the card pressed
# FIXME Bug in here somewhere
def cardInHandPressed(app, x, y):
    for position in 'nsew':
        for card in app.hands[position][::-1]:
            if card != None:
                xCard, yCard = card.location
                if (abs(xCard-x) <= card.cardWidth//2 and
                    abs(yCard-y) <= card.cardHeight//2):
                    print(card, position)
                    return card, position
    return False

def playCard(app, cardAndPosition):
    if cardAndPosition == False: return # returns if card is False
    card, position = cardAndPosition
    # add cards to list of cards played in current round
    app.cardPlayed.append((card, position))
    # removes card from the player's hand
    print(position, card)
    app.hands[position].remove(card)
    # adds card to the player list

def moveCard(card, speed):
    x, y = (700, 400)
    xCard = card.location[0]
    yCard = card.location[1]
    if not (almostEqual(xCard, x, epsilon=1) and 
        almostEqual(yCard, y, epsilon=1)):
        dx = (x-xCard)/10
        dy = (y-yCard)/10
        card.location = (xCard + dx, yCard + dy)


###################################################################
#       Built-in controllers

def appStarted(app):
    playerDict = {'n':'player1', 'e':'player2', 's':'player3', 'w':'player4'}
    app.game = Game(playerDict, 'n')
    app.board = app.game.board
    app.hands = app.board.hands #dict of lists of hands indexed by direction
    app.cardDisplay = 30 # width of card shown (not overlapped) in hand
    app.suitSymbolDict = {'C': '♧', 'D': '♢', 'H': '♡', 'S': '♤'}
    app.backgroundColor = 'green'
    app.cardPlayed = []
    app.handLocations = {'n': (app.width//2, app.height//8),
                         's': (app.width//2, 7*app.height//8),
                         'e': (5*app.width//6, app.height//2),
                         'w': (app.width//6, app.height//2)}
    app.board.locateHands(app.handLocations)
    app.playedCardLocations =  {'n': (app.width//2, app.height//4),
                                's': (app.width//2, 3*app.height//4),
                                'e': (3*app.width//4, app.height//2),
                                'w': (app.width//4, app.height//2)}

def mousePressed(app, event):
    # plays the card pressed
    playCard(app, cardInHandPressed(app, event.x, event.y))
    print(app.cardPlayed)

def timerFired(app):
    # moves card that had been played to the center of the 'table'
    for card, _ in app.cardPlayed:
        #TODO: change this to real card player locations
        moveCard(card, 5)

###################################################################

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                            fill=app.backgroundColor)
    drawHands(app, canvas)
    drawPlayedCard(app, canvas)

###################################################################
#       redrawAll helpers (Primary View)

def drawHands(app, canvas):
    for position in 'nsew':
        for card in app.hands[position]:
            if card.location != None:
                drawCard(app, canvas, card)

def drawPlayedCard(app, canvas):
    for card, _ in app.cardPlayed:
        drawCard(app, canvas, card)

###################################################################
#       helpers of redrawAll helpers (Secondary View) <-- not a technical term

def create_roundedRectangles(canvas, x1, y1, x2, y2, r, fill, outline):
    points = [
        #top left corner
        x1, y1+r,
        x1, y1,
        x1+r, y1,

        # top right corner
        x2-r, y1,
        x2, y1,
        x2, y1+r,

        # bottom right corner
        x2, y2-r,
        x2, y2,
        x2-r, y2,

        #bottom left corner 
        x1+r, y2,
        x1, y2,
        x1, y2-r,
    ]
    canvas.create_polygon(points, smooth=True, fill=fill, outline=outline)

def drawCard(app, canvas, card):
    x, y = card.location
    x -= card.cardWidth//2
    y -= card.cardHeight//2
    # to shift the x, y to the top left of the card
    number = card.number
    suit = card.suit
    color = card.color
    cardWidth = card.cardWidth
    cardHeight = card.cardHeight
    if number > 11:
        number = 'JQKA'[number % 11] #TODO: make into helper function?
    create_roundedRectangles(canvas, x, y, 
                            x+cardWidth, y+cardHeight, 10,
                            'white', 'black')
    canvas.create_text(x+cardWidth//10, y+cardWidth//10, 
                    text=f'{number}\n{app.suitSymbolDict[suit]}', 
                    anchor='nw', justify='center', fill=color)


runApp(width=1350, height=800)

