
from cmu_112_graphics import *
from PIL import ImageTk, Image

#################################

def appStarted(app):
    app.cardWidth = 57
    app.cardHeight = 89
    makeSuits(app)
    

def makeSuits(app):
    app.clubs = '♧'
    app.diamond = '♢'
    app.heart = '♡'
    app.spades = '♤'


def drawCard(app, canvas, x, y, suit, number):
    create_roundedRectangles(canvas, x, y, 
                            x+app.cardWidth, y+app.cardHeight, 10,
                            'white', 'black')
    canvas.create_text(x+app.cardWidth//10, y+app.cardWidth//10, 
                    text=f'{number}\n{suit}', anchor='nw', justify='center')


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


def redrawAll(app, canvas):
    drawCard(app, canvas, 10, 10, app.heart, 4)
    drawCard(app, canvas, 30, 10, app.spades, 'K')
    
    




runApp()