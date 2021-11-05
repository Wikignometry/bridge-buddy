import random


class Card():

    def __init__(self, suit, number): #for now, maybe add values later
        self.suit = suit
        self.number = number
        self.location = None # represented as a tuple of top left 
    
    def __repr__(self):
        if self.number < 11:
            return str(self.number) + self.suit
        return 'JQKA'[self.number % 11] + self.suit

class Board():

    def __init__(self, boardNumber):
        self.boardNumber = boardNumber
        self.dealer = 'wnes'[boardNumber % 4] 
        #wnes because boardNumber starts at 1 (refers to direction)

    def dealHand(self):
        hand = dict()
        cardsPerPlayer = 13
        allCards = self.makeDeck()
        for direction in 'nesw':
            hand[direction] = []
            for _ in range(cardsPerPlayer):
                hand[direction].append(random.choice(allCards))
        self.hand = hand

    def makeDeck(self):
        fullDeck = list()
        for suit in 'SHDC': 
            for number in range(2, 15): # ace is treated as 15
                fullDeck.append(Card(suit, number))
        return fullDeck

class Player():

    def __init__(self, username):
        self.username = username
        self.profileImage = None
        self.bio = None