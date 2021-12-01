# this files contains helper functions
###################################################################
#       Imported Modules
#none
###################################################################


def create_roundedRectangles(canvas, x1, y1, x2, y2, r=10, fill='white', outline='black'):
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
