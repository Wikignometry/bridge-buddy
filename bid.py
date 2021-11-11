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

        super().__init__(dimension=(30, 27), location=(100, 100), 
                        fill=self.color, outline='black',
                        label=f'{self.contract}{self.getSymbol()}',
                        textFill='white') 

    # helps with code testing
    def __eq__(self, other):
        return (isinstance(other, Bid) and 
        (self.contract == other.contract) and
        (self.trump == other.trump))

    #i.e. 6NT, 7H, 1C, 4S, 5D
    def __repr__(self):
        return str(self.contract) + self.trump

    # returns color based on trump suit 
    def getColor(self):
        bidColorDict = {'C': 'green', 'D': 'orange', 'H': 'red', 'S':'blue', 'NT':'grey'}
        return bidColorDict[self.trump]
    
    # returns the drawn version of suit symbols
    def getSymbol(self):
        suitSymbolDict = {'C': '♧', 'D': '♢', 'H': '♡', 'S': '♤', 'NT': 'NT'}
        return suitSymbolDict[self.trump]

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
    assert(bid1.color == 'blue')
    assert(bid1.location == (100, 100))
    assert((bid1.width, bid1.height) == (30, 27))
    assert(bid1.isPressed(112, 110) == True)
    assert(bid1.isPressed(95, 88) == True)
    assert(bid1.isPressed(170, 27) == False)
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


