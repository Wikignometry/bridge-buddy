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

    #TODO: more parameters to come
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
        self.socket.connect((app.HOST, app.PORT))
        print('socketCreated')

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
        print(f'sentCard:{card}')

    # recieves a card from the socket
    def getCard(self):
        cardStr = self.getMessage()
        print(f'gotCard:{cardStr}')
        return Card(int(cardStr[:-1]), cardStr[-1])

    # sends a bid (NT are represented as N)
    def sendBid(self, bid):
        if isinstance(bid, SpecialBid):
            bid = bid.id
        print(f'sendingBid: {bid}')
        self.sendMessage(str(bid)) # so all bids are same length
        print('sentBid')

    # returns an interpreted bid
    def getBid(self):
        print('gettingBid')
        bid = self.getMessage()
        print(f'gotBid:{bid}')
        # for special bids
        if bid == 'Pass' or bid == 'X' or bid == 'XX':
            print('foo')
            return SpecialBid(bid)
        return Bid(int(bid[0]), bid[1:])

    # kinda arbitrary, but for clarity
    def getSeed(self):
        print('gettingSeed')
        seed = float(self.getMessage())
        print(f'my seed is {seed}')
        random.seed(seed)
        print('gotSeed')

    # kinda arbitrary, but for clarity
    def sendSeed(self):
        print('sendingSeed')
        seed = str(random.random())
        self.sendMessage(seed)
        random.seed(seed)
        print('gotSeed')




    
   