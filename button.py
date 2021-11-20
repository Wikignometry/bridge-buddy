###################################################################
#       Imported Files
from cmu_112_graphics import *
from helper import *
###################################################################
# this button class was modified for use in Hack112, but it was originally
# written for use in the term project

# Button is the superclass for every pressable object in the program
#           –> button must be rectangular

class Button():

    def __init__(self, dimension, location=None, action=(lambda: None), 
                fill='blue', outline=None, label=None, textFill='black'):
        # tuples(x, y) of center of button or None 
        self.location = location

        # tuples(width, height)
        self.width, self.height = dimension

        # functions that perform a given action when the button is pressed
        self.action = action

        # color name
        self.fill = fill
        self.outline = outline
        self.label = label
        self.textFill = textFill

        self.fontSize = 12 # int

    # returns True if the button isPressed
    #       –> assumes that button is rectangular (doesn't account for rounded corners)
    def isPressed(self, x, y):
        # to prevent indexOutOfBounds error
        if self.location == None: 
            return False
        return (abs(self.location[0] - x) < self.width/2 and
                abs(self.location[1] - y) < self.height/2)

    # draws a rounded square button
    def draw(self, canvas):
        if self.location == None: return # does not draw if location is None
        x, y = self.location
        create_roundedRectangles(canvas, 
                                x - self.width//2, y - self.height//2,
                                x + self.width//2, y + self.height//2,
                                r=10, fill=self.fill, outline=self.outline)
        if self.label != None:
            canvas.create_text(x, y, 
                        text=f'{self.label}', 
                        font = ('Calbri', self.fontSize),
                        anchor='center', 
                        justify='center', 
                        fill=self.textFill)




###################################################################
#       Test Functions

def testButtonClass():
    print('Testing Button...', end='')
    button1 = Button((5,10), (10,20), lambda: 'foo')
    assert(button1.action() == 'foo')
    assert(button1.location[0] == 10)
    assert(button1.location[1] == 20)
    assert(button1.isPressed(12, 21) == True)
    assert(button1.isPressed(9, 18) == True)
    assert(button1.isPressed(5, 27) == False)
    print('Passed!')

# def appStarted(app):
#     app.button = Button((50,50), (100,100), lambda: print('foo'), fill='royalBlue')

# def mousePressed(app, event):
#     if app.button.isPressed(event.x, event.y):
#         app.button.action()

# def redrawAll(app, canvas):
#     app.button.draw(canvas)

###################################################################
#       Code to run

testButtonClass()
# runApp(width=200, height=200)


