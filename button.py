
# Button is the superclass for every pressable object in the program
#           –> button must be rectangular

class Button():

    def __init__(self, location, dimensions, action):
        # locations are input as tuples(x, y) of center of button
        self.x, self.y = location

        # dimensions are input as tuples(width, height)
        self.width, self.height = dimensions

        # actions are functions that perform a given action when the button is pressed
        self.action = action

    # returns True if the button isPressed
    #       –> assumes that button is rectangular (doesn't account for rounded corners)
    def isPressed(self, x, y):
        return (abs(self.x - x) < self.width/2 and
                abs(self.y - y) < self.height/2)


###################################################################
#       Test Functions

def testButtonClass():
    print('Testing Button...', end='')
    button1 = Button((10,20), (5,10), lambda: 'foo')
    assert(button1.action() == 'foo')
    assert(button1.x == 10)
    assert(button1.y == 20)
    assert(button1.isPressed(12, 21) == True)
    assert(button1.isPressed(9, 18) == True)
    print('Passed!')

###################################################################
#       Code to run

testButtonClass()


