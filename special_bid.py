###################################################################
#       Imported Files
from button import *
# 112_graphs, button, and draw_helpers imported via bid
###################################################################

class SpecialBid(Button):

    def __init__(self, id):
        self.id = id
        if self.id == 'Pass':
            super().__init__((50, 27), label='Pass', fill='dark green', 
                            outline='white', textFill='white')
        elif self.id == 'X': #double
            super().__init__((30, 27), label='X', fill='red', 
                            outline='white', textFill='white')
        else: #self.id == 'XX' (redouble)
            super().__init__((30, 27), label='XX', fill='light blue', 
                            outline='white', textFill='white')

    def locate(self, location):
        xCenter, yCenter = location
        if self.id == 'Pass':
            self.location = (xCenter - 50, yCenter + 100)
        elif self.id == 'X':
            self.location = (xCenter + 10, yCenter + 100)
        else:
            self.location = (xCenter + 50, yCenter + 100)

    def __repr__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, SpecialBid):
            return (self.id == other.id)
        else: 
            return False

    
