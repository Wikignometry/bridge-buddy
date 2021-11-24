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
                            outline='black', textFill='white')

    def locate(self, location):
        xCenter, yCenter = location
        if self.id == 'Pass':
            self.location = (xCenter - 50, yCenter + 100)

    def __repr__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, SpecialBid):
            return (self.id == other.id)
        else: 
            return False

    
