# this files contains helper functions

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

# both functions below from http://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
# only used for debuggin purposes, will be removed for final submission
def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def print2dList(L):
    print(repr2dList(L))
