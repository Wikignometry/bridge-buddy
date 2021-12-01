###################################################################
#       Imported Files
from button import *
# 112_graphs and draw_helpers imported via button
###################################################################


class Bid(Button):

    def __init__(self, contract, trump):

        # int – number of tricks over half (6) the declaring side must get for a positive score)
        self.contract = contract
        # 'C', 'D', 'H', 'S' or 'NT' (no trump)
        self.trump = trump 

        self.color = self.getColor() # color names

        outline='black'

        super().__init__(dimension=(30, 27), location=(100, 100), 
                        fill=self.color, outline=outline,
                        label=f'{self.contract}{self.getSymbol()}',
                        textFill=outline) 

    # helps with code testing
    def __eq__(self, other):
        return (isinstance(other, Bid) and 
        (self.contract == other.contract) and
        (self.trump == other.trump))

    #i.e. 6NT, 7H, 1C, 4S, 5D
    def __repr__(self):
        return str(self.contract) + self.trump

    # makes Bid hashable based on contract and trump
    def __hash__(self):
        return hash(str(self))

    # makes < works
    def __lt__(self, other):
        suitOrder = ['NT', 'S', 'H', 'D', 'C'] # order from greatest to least
        if self.contract == other.contract:
            return suitOrder.index(self.trump) > suitOrder.index(other.trump)
        else:
            return self.contract < other.contract

    # returns color based on trump suit 
    def getColor(self):
        bidColorDict = {'C': '#06D6A0', 'D': '#FFC847', 'H': '#F36888', 'S':'#32BDEC', 'NT':'#9197A1'}
        return bidColorDict[self.trump]
    
    # returns the drawn version of suit symbols
    def getSymbol(self):
        suitSymbolDict = {'C': '♧', 'D': '♢', 'H': '♡', 'S': '♤', 'NT': 'NT'}
        return suitSymbolDict[self.trump]

    # returns True if is game
    def isGame(self):
        return ((self.trump in 'HS' and self.contract >= 4) or
                (self.trump in 'DC' and self.contract >= 5) or
                (self.trump == 'NT' and self.contract >= 3))

    # returns the game bid for each suit
    def suitGame(self):
        if self.trump in 'HS':
            return Bid(4, self.trump)
        if self.trump in 'DC':
            return Bid(5, self.trump)
        if self.trump == 'NT':
            return Bid(3, self.trump)

    def draw(self, canvas):
        super().draw(canvas)
        # x, y = self.location
        # canvas.create_text(x, y, 
        #             text=f'{self.contract}{self.getSymbol()}', 
        #             anchor='center', justify='center', fill='white')




###################################################################
#       Test Functions

def testBidClass():
    print('Testing Bid...', end='')
    bid1 = Bid(5,'S')
    assert(bid1.location == (100, 100))
    assert((bid1.width, bid1.height) == (30, 27))
    assert(bid1.isPressed(112, 110) == True)
    assert(bid1.isPressed(95, 88) == True)
    assert(bid1.isPressed(170, 27) == False)
    assert(Bid(4,'H')<Bid(4,'S'))
    assert(Bid(5,'H')>Bid(4,'S'))
    assert(Bid(5,'H').isGame())
    assert(not Bid(3,'D').isGame())
    assert( Bid(3,'NT').isGame())
    print('Passed!')

# def appStarted(app):
#     app.bid = Bid(5,'S')

# def mousePressed(app, event):
#     if app.bid.isPressed(event.x, event.y):
#         print('yes!')

# def redrawAll(app, canvas):
#     app.bid.draw(canvas)

###################################################################
#       Code to run

testBidClass()
# runApp(width=200, height=200)


