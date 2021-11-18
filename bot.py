# bot class (contains Monte Carlo methods)
###################################################################
#       Imported Files
from player import *
from node import *
# 112_graphs, random, card, bid, board, copy
# special_bid, helper, button, heuristic imported via node
###################################################################
# the idea for using monte carlo experiments on a double-dummy solver
# came from https://en.wikipedia.org/wiki/Computer_bridge

class Bot():

    def __init__(self, position, depth, breadth):
        self.position = position # str of position
        self.history = []
        self.possibleNodes = [] # list of Nodes
        self.depth = depth # int of depth the bot will search
        self.bid = None
        self.hand = [] # list of Cards in the bot's hand
        self.breadth = breadth # refers to the number of Monte Carlo simulations to run

        self.knownCards = [] # list of cards we've seen (and therefore cannot be in opponent's hands)

    def assignBid(self, bid):
        self.bid = bid


        

    # def makeNode(self, hands, depth, activePosition, currentRound, nsTricks, ewTricks, bid):
    #     self.node = Node(hands, depth, activePosition, currentRound, nsTricks, ewTricks, bid)

    # def botTurn(self):
    #     self.node.calculateMinimax(True, baseHeuristic)
    #     return self.node.getPlay()

    # actions to perform when the board is started
    def startPlay(self, hand):
        print('startPlay')
        self.hand = copy.deepcopy(hand)
        self.knownCards = self.knownCards + self.hand

    # simulate new Monte Carlo hands and returns chosen card     
    def playTurn(self, currentRound, nsTricks, ewTricks):
        self.possibleNodes = []
        self.simulate(currentRound, nsTricks, ewTricks)
        cardPicked = self.getCard()
        self.hand.remove(cardPicked)
        return cardPicked

    # generates Monte Carlo that fits known information
    def simulate(self, currentRound, nsTricks, ewTricks):
        for _, card in currentRound:
            self.knownCards.append(card)
        for _ in range(self.breadth):
            self.generateMonteCarlo(currentRound, nsTricks, ewTricks)

    # aggregates the cards from each node to get the modal card choice
    def getCard(self):
        # gets a dict of card mapped to number of times picked
        print(self.hand)
        cardCount = {'base': 0}
        print(len(self.possibleNodes[0].hands[self.position]))
        for node in self.possibleNodes:
            node.calculateMinimax(self.position in 'ns', baseHeuristic)
            proposedPlay = node.getPlay()
            value = cardCount.get(proposedPlay, 0)
            cardCount[proposedPlay] = value + 1
        print(cardCount)

        # get the modal card picked
        cardPick = 'base'
        for card in cardCount: #TODO: this feels so ugly
            if cardCount[card] > cardCount[cardPick]:
                cardPick = card
        print(cardPick)

        return cardPick
            
    # # TODO: update monte carlo when dummy reveals hand
    # def endBidding(self):
    #     pass

    # maybe #TODO? couldn't get this to work yet
    # # prunes Monte Carlo when a card becomes available    
    # def updateMonteCarlo(self, currentRound, nsTricks, ewTricks):
    #     # updating based on the cards played in the round
    #     for position, card in currentRound: 
    #         print(position, card)   
    #         for i in range(len(self.possibleNodes)):
    #             print(self.possibleNodes[i].hands[position])
    #             # if card shown does not correspond with guess, pop the possible Node and generate a new one
    #             if card not in self.possibleNodes[i].hands[position]:
    #                 self.possibleNodes.pop(i)
    #                 self.generateMonteCarlo(currentRound, nsTricks, ewTricks) # appends new node to possible nodes
    #             # check what card the bot played and update the nodes accordingly
    #             self.possibleNodes[i] = self.possibleNodes[i].children[card] 

               
    # appends a new MonteCarlo-ed node to possibleNodes
    def generateMonteCarlo(self, currentRound, nsTricks, ewTricks):
        montyHands = dict()
        montyHands[self.position] = self.hand
        otherCards = self.makeUnkownDeck() # deck with known cards removed
        cardsPerPlayer = len(otherCards)//4 + 1
        if currentRound != []:
            leader = currentRound[0][0]
        else: leader = self.position
            # in case there is an uneven number of cards
        dealOrder = 'nesw'['nesw'.index(leader):] + 'nesw'[:'nesw'.index(leader)]
        for direction in dealOrder:
            if direction != self.position:
                montyHands[direction] = []
                for _ in range(cardsPerPlayer):
                    if otherCards == []: break
                    dealtCard = random.choice(otherCards) 
                    otherCards.remove(dealtCard) # prevents the card from being dealt twice
                    montyHands[direction].append(dealtCard)
        self.possibleNodes.append(Node(montyHands, self.depth, self.position, 
                                        currentRound, nsTricks, ewTricks, self.bid 
        ))

    # returns a deck with all the cards not in hand
    def makeUnkownDeck(self):
        deck = makeDeck()
        for card in self.knownCards:
            deck.remove(card)
        return deck

    
