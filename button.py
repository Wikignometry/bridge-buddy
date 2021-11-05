
# Button is the superclass for every pressable object in the program
#           –> button must be rectangular

class Button():

    def __init__(self, location, dimensions, action):
        # tuples(x, y) of center of button or None 
        self.location = location

        # tuples(width, height)
        self.width, self.height = dimensions

        # functions that perform a given action when the button is pressed
        self.action = action

    # returns True if the button isPressed
    #       –> assumes that button is rectangular (doesn't account for rounded corners)
    def isPressed(self, x, y):
        # to prevent indexOutOfBounds error
        if self.location == None: 
            return False
        return (abs(self.location[0] - x) < self.width/2 and
                abs(self.location[1] - y) < self.height/2)

#TODO: setLocation function

###################################################################
#       Test Functions

def testButtonClass():
    print('Testing Button...', end='')
    button1 = Button((10,20), (5,10), lambda: 'foo')
    assert(button1.action() == 'foo')
    assert(button1.location[0] == 10)
    assert(button1.location[1] == 20)
    assert(button1.isPressed(12, 21) == True)
    assert(button1.isPressed(9, 18) == True)
    assert(button1.isPressed(5, 27) == False)
    print('Passed!')

###################################################################
#       Code to run

testButtonClass()


