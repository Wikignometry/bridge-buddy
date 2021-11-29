# creates the class Sound
###################################################################
#       Imported Modules

import pygame
from cmu_112_graphics import *
###################################################################
# The following links were referenced to varying degrees:
# https://gamedev.stackexchange.com/questions/64472/whats-the-difference-between-pygames-sound-and-music-classes
# https://stackoverflow.com/questions/42393916/how-can-i-play-multiple-sounds-at-the-same-time-in-pygame
# https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound


# for sound effects (file must be in wav format)
class Sound():

    def __init__(self, path):
        self.path = path
        self.loops = 0
        self.audio = pygame.mixer.Sound(path)
        self.name = None # assigned for some music in this program

    def start(self, loops=0):
        self.loops = loops
        self.audio.play(loops=loops)

    def __eq__(self, other):
        if isinstance(other, Sound):
            return self.path == other.path
        return False



# modified from http://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSoundsWithPygame
class Music(Sound):

    def __init__(self, path=False):
        self.path = path
        self.loops = 1

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        if not self.path: return
        # so we can have different music
        pygame.mixer.music.load(self.path)
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        if not self.path: return
        pygame.mixer.music.stop()


###################################################################
#       Test Functions

# def appStarted(app):
#     pygame.mixer.init()
#     app.sound = Sound("media/mouse_click.mp3")

# def appStopped(app):
#     app.sound.stop()

# def keyPressed(app, event):
#     if (event.key == 's'):
#         if app.sound.isPlaying(): app.sound.stop()
#         else: app.sound.start()
#     elif (event.key == 'l'):
#         app.sound.start(loops=-1)
#     elif event.key.isdigit():
#         app.sound.start(loops=int(event.key))

# def timerFired(app):
#     pass

# def redrawAll(app, canvas):
#     canvas.create_text(app.width/2, app.height/2-60,
#                        text=f'{app.sound.path} (loops = {app.sound.loops})',
#                        font='Arial 30 bold', fill='black')
#     canvas.create_text(app.width/2, app.height/2-20,
#                        text=f'sound is playing = {app.sound.isPlaying()}',
#                        font='Arial 30 bold', fill='black')
#     canvas.create_text(app.width/2, app.height/2+20,
#                        text='Press s to start/stop sound',
#                        font='Arial 30 bold', fill='black')
#     canvas.create_text(app.width/2, app.height/2+60,
#                        text='Press l to loop sound',
#                        font='Arial 30 bold', fill='black')

# runApp(width=600, height=200)
