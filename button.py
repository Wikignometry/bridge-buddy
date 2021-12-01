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

    def __init__(self, dimension, location=None, action=None, 
                fill='blue', outline=None, label=None, textFill='black', 
                r=10, fontSize=12, textAnchor='center', font='Calbri', style='roman',
                overlay=None, overlayLocation=(0,0), overlayAlpha=254, overlayScale=1
                ):
        
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

        self.font = font
        self.style = style # bold underline italics roman
        self.fontAnchor = textAnchor # supports center and se

        # int
        self.r = r 
        self.fontSize = fontSize 

        self.overlay = overlay
        self.overlayLocation = overlayLocation
        self.overlayAlpha = overlayAlpha # transparency of image
        self.overlayScale = overlayScale # scale of the image
        if self.overlay != None:
            self.getOverlay(overlay)

    # process the overlay image
    def getOverlay(self, path):
        self.overlay = Image.open(path)
        self.overlay = self.scaleImage(self.overlay, self.overlayScale)
        if path[-3:] == 'png':
            # based on https://github.com/python-pillow/Pillow/issues/4687
            # makes the image translucent without displaying already transparent pixels
            overlayCopy = self.overlay.copy()
            overlayCopy.putalpha(self.overlayAlpha) # increases transparency
            self.overlay.paste(overlayCopy, self.overlay)
        else: # normal transparency for non-transparent images
            self.overlay.putalpha(self.overlayAlpha)
        if self.location != None:
            xButton, yButton = self.location
            width, height = self.overlay.size
            x, y = xButton + self.overlayLocation[0], yButton + self.overlayLocation[1]
            lowX, lowY, highX, highY = 0, 0, width, height # default values
            if x-width/2 <= xButton-self.width/2:
                lowX = (xButton-self.width//2) - (x-width//2) + self.overlayLocation[0]
            if x+width/2 >= xButton+self.width/2:
                highX = width-((x+width//2) - (xButton+self.width//2) - self.overlayLocation[0])
            if y-height/2 <= yButton-self.height/2:
                lowY = (yButton-self.height//2) - (y-height//2) + self.overlayLocation[1]
            if y+height/2 >= yButton+self.height/2:
                highY = height - ((y+height//2) - (yButton+self.height//2) - self.overlayLocation[1])
            self.overlay = self.overlay.crop((lowX, lowY, highX, highY))



    # copied directly from cmu_112_graphics
    def scaleImage(self, image, scale, antialias=False):
        # antialiasing is higher-quality but slower
        resample = Image.ANTIALIAS if antialias else Image.NEAREST
        return image.resize((round(image.width*scale), round(image.height*scale)), resample=resample)

    def __repr__(self):
        if self.label != None:
            return self.label
        elif self.action != None:
            return self.action.__name__
        else: return 'unknown button'


    def __eq__(self, other):
        if (isinstance(other, Button) and (self.action == None or other.action == None)):
            return False
        return self.action == other.action

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
                                r=self.r, fill=self.fill, outline=self.outline)
        
        
        if self.overlay != None:
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.overlay))


        if self.label != None:
            if self.fontAnchor == 'center':
                canvas.create_text(x, y, 
                        text=f'{self.label}', 
                        font = (self.font, self.fontSize, self.style),
                        anchor='center', 
                        justify='center', 
                        fill=self.textFill)
            else:
                margin=10
                canvas.create_text(x+self.width//2-margin, y+self.height//2-margin, 
                        text=f'{self.label}', 
                        font = (self.font, self.fontSize, self.style),
                        anchor='se', 
                        justify='right', 
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


