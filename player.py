# Player is the class for all human players, and the superclass for the AI

class Player():

    #TODO: more parameters to come
    def __init__(self, username):
        self.username = username

    def __eq__(self, other):
        return isinstance(other, Player) and self.username == other.username

    