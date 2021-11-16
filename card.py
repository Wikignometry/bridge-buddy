###################################################################
#       Imported Files
from button import *
import math
# 112_graphs and draw_helpers imported via button
###################################################################

class Card(Button):

    def __init__(self, number, suit):

        self.suit = suit # 'C', 'D', 'H', or 'S'
        self.number = number # int, (jack –> ace) = (11 –> 14)
        
        self.setColor() # self.color: 'red' or 'black'

        self.location = None # tuple(x, y) or None
        self.targetLocation = None # where it wants to go

        super().__init__(dimension=(57,89), 
                        fill='white',
                        outline='black')

    # helps with code testing
    def __eq__(self, other):
        return (isinstance(other, Card) and
                (self.number == other.number) and
                (self.suit) == other.suit)

    # i.e. 3C, AS, 10H, JD, 8H
    def __repr__(self):
        if self.number < 11:
            return str(self.number) + self.suit
        return 'JQKA'[self.number % 11] + self.suit

    

    # will crash if fed non-Card other argument
    # orders by suit first, then number
    def __lt__(self, other):
        suitOrder = 'SHCD' # order from greatest to least
        if suitOrder.find(self.suit) == suitOrder.find(other.suit):
            return (self.number < other.number)
        else:
            return suitOrder.find(self.suit) > suitOrder.find(other.suit)

    # returns True is self is greater than other
    def isGreaterThanInGame(self, other, bid, lead):
        leadSuit = lead.suit
        trump = bid.trump
        if self.suit == other.suit:
            return (self.number > other.number)
        else:
            if self.suit == trump or other.suit == trump:
                return self.suit == trump
            elif self.suit == leadSuit or other.suit == leadSuit:
                return self.suit == leadSuit
            else: return True # this is arbitrary, neither card can win in this circumstance

    # assigns color to card based on suit
    def setColor(self):
        if self.suit in 'DH': 
            self.color = 'red'
        else: 
            self.color = 'black'

    # returns the drawn version of suit symbols
    def getSymbol(self):
        suitSymbolDict = {'C': '♧', 'D': '♢', 'H': '♡', 'S': '♤'}
        return suitSymbolDict[self.suit]

    # returns the number (or AKQJ symbol) 
    def getNumber(self):
        if self.number > 10:
            return ('JQKA'[self.number % 11])
        return self.number

    # changed the location of the card towards a given value
    def move(self, speed):
        if self.location == None or self.targetLocation == None: return 
        x0, y0 = self.location
        x1, y1 = self.targetLocation
        if not (math.isclose(x0, x1, abs_tol=0.1) and
            math.isclose(y0, y1, abs_tol=0.1)):
            dx = int((x1-x0)*speed) + 1 # speed is a value between 1 and 0
            dy = int((y1-y0)*speed) + 1
            self.location = (x0 + dx, y0 + dy)   

    # will override button draw method
    def draw(self, canvas):
        if self.location == None: 
            return
        super().draw(canvas)
        x, y = self.location
        canvas.create_text(x - self.width//2 + self.width//10, 
                    y - self.height//2 + self.height//10, 
                    text=f'{self.getNumber()}\n{self.getSymbol()}', 
                    anchor='nw', justify='center', fill=self.color)


    # returns True if list contains the suit of the card
    def containsSuit(self, cardList):
        for card in cardList:
            if card.suit == self.suit:
                return True
        return False

###################################################################
#       Test Functions

def testCardClass():
    print('Testing Card...', end='')
    card1 = Card(5, 'C')
    assert(str(card1) == '5C')
    assert(card1.location == None)
    assert(card1.color == 'black')
    assert((card1.width, card1.height) == (57, 89))
    card1.location = (15, 20)
    assert(card1.location == (15, 20))
    assert(card1.isPressed(16, 24) == True)
    assert(card1.isPressed(200, 500) == False)
    assert((Card(5, 'C') > Card(4,'C')) == True)
    assert((Card(5, 'C') > Card(7,'C')) == False)
    assert((Card(5, 'C') < Card(7,'H')) == True)
    assert((Card(7, 'C') < Card(4,'H')) == True)
    assert((Card(8, 'S') < Card(8,'C')) == False)
    assert((Card(8, 'H') < Card(8,'S')) == True)
    assert(sorted([Card(7, 'H'), Card(5, 'H'), Card(6, 'H')]) == [Card(5, 'H'), Card(6, 'H'), Card(7, 'H')])
    assert(sorted([Card(5, 'D'), Card(7, 'H'), Card(6, 'C')]) == [Card(5, 'D'), Card(6, 'C'),Card(7, 'H')])
    assert(sorted([Card(5, 'S'), Card(6, 'H'), Card(4, 'H')]) == [Card(4, 'H'), Card(6, 'H'),Card(5, 'S')])
    print('Passed!')

# def appStarted(app):
#     app.card1 = Card(4,'C')
#     app.card2 = Card(14,'H')
#     app.card1.location = (200, 200)
#     app.card2.location = (200, 300)

# def timerFired(app):
#     app.card1.move(100,100, 0.1)
#     app.card2.move(100,100, 0.1)

# def redrawAll(app, canvas):
#     app.card1.draw(canvas)
#     app.card2.draw(canvas)

###################################################################
#       Code to run

testCardClass()
# runApp(width=500, height=500)

