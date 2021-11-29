from cmu_112_graphics import *




'''
def redrawAll(app, canvas):
    t = app.textBoxText
    while True:
        tid = canvas.create_text(x, y, text=t)
        x0, y0, x1, y1 = canvas.bbox(tid)
        if x1 - x0 < w:
            break
        t = t[1:]
        canvas.delete(tid)
'''