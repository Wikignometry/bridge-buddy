# Player is the class for all human players (including remote ones)
###################################################################
#       Imported Modules
from card import * # button imported via card
from bid import *
from special_bid import *
import socket
import random
###################################################################
#  

class Player():

    def __init__(self, username):
        self.username = username
        self.socket = None # a socket object


    def __eq__(self, other):
        return isinstance(other, Player) and self.username == other.username

 ###################################################################
#   for server only

    def acceptSocket(self, app):
        self.socket = app.server.accept()[0]

###################################################################
#   for clients only

    # creates and connects a new socket
    def createSocket(self, app):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(10) # timeout after 5 seconds
        # settimeout from https://stackoverflow.com/questions/3432102/python-socket-connection-timeout
        self.socket.connect((app.HOST, app.PORT))

###################################################################
#   for both

    # send message to socket
    def sendMessage(self, message):
        self.socket.send(message.encode('utf-8'))

    # get message from socket
    def getMessage(self):
        return self.socket.recv(1024).decode('utf-8')
    
    # send card to socket
    def sendCard(self, card):
        self.sendMessage(str(card.number)+card.suit)

    # recieves a card from the socket
    def getCard(self):
        cardStr = self.getMessage()
        return Card(int(cardStr[:-1]), cardStr[-1])

    # sends a bid (NT are represented as N)
    def sendBid(self, bid):
        if isinstance(bid, SpecialBid):
            bid = bid.id
        self.sendMessage(str(bid)) # so all bids are same length

    # returns an interpreted bid
    def getBid(self):
        bid = self.getMessage()
        # for special bids
        if bid == 'Pass' or bid == 'X' or bid == 'XX':
            return SpecialBid(bid)
        return Bid(int(bid[0]), bid[1:])

    # kinda arbitrary, but for clarity
    def getSeed(self):
        seed = float(self.getMessage())
        random.seed(seed)

    # kinda arbitrary, but for clarity
    def sendSeed(self):
        seed = str(random.random())
        self.sendMessage(seed)
        random.seed(seed)




    
   