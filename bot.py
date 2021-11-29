# bot class (contains Monte Carlo methods)
###################################################################
#       Imported Files
from player import *
from node import *
from special_bid import *
# 112_graphs, random, card, bid, board, copy
# special_bid, helper, button, heuristic imported via node
###################################################################
# the idea for using monte carlo experiments on a double-dummy solver
# came partially from https://en.wikipedia.org/wiki/Computer_bridge

class Bot():

    def __init__(self, position, depth, breadth):
        self.position = position # str of position
        self.history = []
        self.possibleNodes = [] # list of Nodes
        self.depth = depth # int of depth the bot will search
        self.bid = None
        self.hand = [] # list of Cards in the bot's hand
        self.breadth = breadth # refers to the number of Monte Carlo simulations to run

        self.knownCards = set() # set of cards we've seen (and therefore cannot be in opponent's hands)
        self.cheater = False #boolean to indicate whether the bot can look at other players cards

        self.dummy = None # turns into a position once dummy is finalized
        self.dummyHand = None # turns into a list of Cards

###################################################################
# bidding

    def assignBid(self, bid):
        self.bid = bid

    # interprets hands for bidding purposes
    def interpretInitialHand(self, hand):
        self.hand = hand
        self.points = self.getHandPoints() # points in our hand
        self.partner = self.getPartner()
        self.distribution = self.getDistribution(self.hand) 
        self.partnerDistribution = self.initialOtherDistribution() 
        self.partnerPoints = (0, 37) # min max inclusive of potential partner points range
        # partnerDistribution is a dict where key=suit and value=tuple(min, max)
        # min and max in inclusive
        self.forcing = False # otherwise, Bid
        self.conventionUsed = None # 's' for stayman, 'j' for jacoby
        # print(self.position, self.distribution, self.points)

    # updates the distribution information based on bidding data
    def updateDistribution(self, otherDistribution, suit, min, max):
        oldMin, oldMax = otherDistribution[suit]
        if min > oldMin:
            otherDistribution[suit] = (min, otherDistribution[suit][1])
        if max < oldMax:
            otherDistribution[suit] = (otherDistribution[suit][0], max)

    # returns an updated narrower range of points
    def updatePoints(self, points, min, max):
        oldMin, oldMax = points
        if min > oldMin:
            points = (min, points[1])
        if max < oldMax:
            points = (points[0], max)
        return points


    # returns the partner given a position
    def getPartner(self):
        pair = [['n', 's'], ['e', 'w']][int(self.position in 'ew')]
        pair.remove(self.position)
        return pair[0]

    # returns a dict of the distribution of cards
    def getDistribution(self, hand):
        distribution = {'S': 0, 'H': 0, 'D': 0, 'C': 0}
        for card in hand:
            distribution[card.suit] += 1
        return distribution

    # creates a dict of min and max distribution (0, 13)
    def initialOtherDistribution(self):
        distribution = dict()
        for suit in 'SHDC':
            distribution[suit] = (0, 13)
        return distribution

    # returns the bid to be played
    def playBid(self, bids): # bids are list of tuple (position, bid)
        
        self.bids = bids

        # returns the number of rounds that we have bidded
        self.round = self.getBiddingRound(bids)
        
        if self.hasNoBids(bids):
            return self.getOpeningBid() # returns the first 

        elif self.firstBid(bids)[0] == self.partner: # firstBidPosition = self.partner
            self.interpretPartnerBids(bids)
            return self.getRespondingBid(bids)

        elif self.firstBid(bids)[0] == self.position: # firstBidPosition = self.position
            self.interpretPartnerResponse()
            return self.getOpenersBid()
        # if you don't know what to do, pass
        return SpecialBid('Pass')
        # else:
        #     return self.getDefendingBid(bids)


    def getOpenersBid(self):
        if self.round == 1:
            return self.firstRebid()
        else:
            return self.otherRebid()


    def interpretPartnerResponse(self):
        self.getBidCategory()
        #TODO:


    def firstRebid(self):
        
        opening = self.getBid(self.partner, 1, self.bids)
        response = self.getBid(self.partner, 1, self.bids)
        if response == SpecialBid('Pass'):
            return SpecialBid('Pass')

        elif self.biddingCategory == 'NT':
            if response.trump == 'C': # stayman
                if self.distribution['H'] >= 4:
                    return self.getMinimumBidInSuit('H')
                elif self.distribution['S'] >= 4:
                    return self.getMinimumBidInSuit('S')
                else:
                    return self.getMinimumBidInSuit('D')
            else: # jacoby transfer
                return self.getMinimumBidInSuit(['NT', 'S', 'H', 'D', 'C'].index(response.trump) + 1)
        elif self.biddingCategory == 'weak':
            if response.trump == 'NT':
                if self.points <= 8:
                    return self.getMinimumBidInSuit('NT') # skipping features description
                else:
                    return self.getMinimumBidInSuit(opening.trump)
        elif self.biddingCategory == 'strong':
            if response == Bid(2, 'D'):
                if 22 < self.points < 24 and self.isEvenDistribution():
                    return self.getMinimumBidInSuit('NT')
                else:
                    return self.otherResponse()
        else: # normal
            if 12 <= self.points <= 14:
                if self.isEvenDistribution():
                    return self.getMinimumBidInSuit('NT')
                # rebid suit
                elif ((self.distribution[opening.trump] >= 6 and opening.trump in 'HS') or 
                    (self.distribution[opening.trump] >= 4 and opening.trump in 'DC')):
                    return self.getMinimumBidInSuit(opening.trump)
                elif self.distribution[response.trump] >= 3:
                    return self.getMinimumBidInSuit(response.trump)
                else:
                    maxSuit = 'C' # arbitrary
                    for suit in self.distribution:
                        if (self.distribution[maxSuit] > self.distribution[suit] and 
                            suit != opening.trump):
                            maxSuit = suit
                    return self.getMinimumBidInSuit(maxSuit)
        return SpecialBid('Pass')


    # return the number of rounds we have bidded
    def getBiddingRound(self, bids):
        count = 0
        for position, _ in bids:
            if position == self.position:
                count += 1
        return count

    # get the position's nth bid
    def getBid(self, position, n, bids):
        for bidder, bid in bids:
            if bidder == position:
                n -= 1
                if n == 0:
                    return bid

    def getLastBid(self, bids, position='nsew'):
        for bidder, bid in bids[::-1]:
            if isinstance(bid, Bid) and bidder in position:
                return bid

    # get bid when partner opens
    def getRespondingBid(self, bids):
        if self.round == 0:
            return self.firstResponse(bids)
        else:
            return self.otherResponse(bids)

    # response to any partner bid after the opening
    def otherResponse(self, bids):
        print(f'otherResponse:{self.bids[:-2][1]}')
        if self.conventionUsed == 'b': #blackwood
            if self.hasFullAces() and self.getLastBid().contract == 5:
                if self.getTotalPoints() > 40: # grand slam points
                    return Bid(5, 'NT')
                else:
                    return Bid(6, self.longestSuitInPartnership())
            elif self.hasFullKings() and self.getLastBid().contract == 6:
                return Bid(7, self.longestSuitInPartnership())
            else:
                return self.getMinimumBidInSuit(self.longestSuitInPartnership(), bids)
        elif self.isMinimumSlam():
            self.conventionUsed = 'b'
            return Bid(4, 'NT')
        elif self.isMinimumGame(self.longestSuitInPartnership()):
            return Bid(1, self.longestSuitInPartnership()).suitGame()
    
    def hasFullAces(self):
        aceCount = 0
        for card in self.hand:
            if card.number == 14:
                aceCount += 1
        return aceCount == 4 # over 4 may mean that it's 0, not 4 kings

    def hasFullKings(self):
        kingCount = 0
        for card in self.hand:
            if card.number == 13:
                kingCount += 1
        return kingCount == 4 # over 4 may mean that it's 0, not 4 kings


    # returns the total minimum points between the pair
    def getTotalPoints(self):
        return self.points + self.partnerPoints[0]

    # first response to partner's opening bid
    def firstResponse(self, bids):
        opening = self.getBid(self.partner, 1, bids)
        if self.biddingCategory == 'NT':
            if (self.distribution['S'] >= 5 or 
                self.distribution['H'] >= 5 or 
                (self.distribution['S'] <= 4 and
                self.distribution['H'] <= 4)):

                self.conventionUsed = 'j'
                longestSuit = self.longestSuitInHand()
                jacobySuit = ['NT', 'S', 'H', 'D', 'C'][['NT', 'S', 'H', 'D', 'C'].index(longestSuit) - 1]
                return self.getMinimumBidInSuit(jacobySuit)
            else:  
                self.conventionUsed = 's' #stayman
                return self.getMinimumBidInSuit('C', bids)
        elif self.biddingCategory == 'strong':
            if self.points > 8:
                if self.isEvenDistribution():
                    return self.getMinimumBidInSuit('NT', bids)
                for suit in 'HSCD':
                    if self.distribution[suit] > 5:
                        if suit == 'D':
                            return Bid(3, 'D')
                        return self.getMinimumBidInSuit(suit, bids)
            return self.getMinimumBidInSuit('D')
        elif self.biddingCategory == 'weak':
            if self.isMinimumGame(opening.trump):
                return Bid(2, 'NT')
            else:
                return SpecialBid('Pass')
        else: #normal
            if (
                (opening.trump in 'HS' and 
                self.distribution[opening.trump] >= 3) 
                or
                (opening.trump in 'CD' and 
                self.distribution[opening.trump] >= 4 and 
                self.longestSuitInHand() in 'CD')
                ):
                return self.getMinimumBidInSuit(opening.trump, bids)
            else:
                return self.getMinimumBidInSuit(self.longestSuitInHand(), bids)

    # returns longest suit in the partnership based on min values
    def longestSuitInPartnership(self):
        maxSuit = 'S' # arbitrary
        for suit in self.distribution:
            if self.distribution[maxSuit] + self.partnerDistribution[maxSuit][0] < self.distribution[suit] + self.partnerDistribution[suit][0]:
                maxSuit = suit
        return maxSuit

    # returns the longest suit in the hand
    def longestSuitInHand(self):
        maxSuit = 'S' # arbitrary
        for suit in self.distribution:
            if self.distribution[maxSuit] < self.distribution[suit]:
                maxSuit = suit
        return maxSuit

    # returns True if the the partnership is definitely in game        
    def isMinimumGame(self, suit):
        totalPoints = self.points + self.partnerPoints[0] # the minimum number of points partner may have
        if suit == None:
            return totalPoints >= 24 
        elif suit in 'HS':
            return totalPoints >= 24 
        elif suit == 'NT':
            return totalPoints >= 25
        else:
            return totalPoints >= 27
    
    # returns True if enough points for slam, returns False otherwise 
    #TODO double check slam value
    def isMinimumSlam(self):
        totalPoints = self.points + self.partnerPoints[0] # the minimum number of points partner may have
        return totalPoints > 32

    # evaluates known values of partner's hand
    def interpretPartnerBids(self, bids):
        if self.getLastBid == SpecialBid('Pass'): # don't interpret passes
            return
        elif self.round == 0:
            print('round 0')
            self.interpretPartnerFirstBid(bids)
        elif self.round == 1:
            self.interpretPartnerRebid(bids)
        else:
            self.interpretEndRebids(bids)

    def interpretEndRebids(self, bids):
        lastBid = self.getLastBid(bids, self.partner)
        if self.conventionUsed == 'b':
            cardCount = {
                'C': 4, # this is either 0 or 4
                'D': 1,
                'H': 2,
                'S': 3,
                'NT': 0 # not a real bid, but in case someone fails
            }
            if lastBid.contract == 5:
                self.partnerKingCount = cardCount[lastBid.trump]
            elif lastBid.contract == 6:
                self.partnerAce = cardCount[lastBid.trump]
        elif Bid(lastBid.suitGame().contract - 1, lastBid.trump):
            self.cueBid = True


    def interpretPartnerRebid(self, bids):
        opening = self.getBid(self.partner, 1, bids)
        response = self.getBid(self.position, 1, bids) # our bid
        rebid = self.getBid(self.partner, 2, bids) # partner's bid
        if self.biddingCategory == 'NT':
            if self.conventionUsed == 's': # stayman convention
                self.conventionUsed = None # so it only reads stayman once
                if rebid.trump == 'S':
                    self.updateDistribution(self.partnerDistribution, 'S', 4, float('inf'))
                    self.updateDistribution(self.partnerDistribution, 'H', 0, 4)
                elif rebid.trump == 'H':
                    self.updateDistribution(self.partnerDistribution, 'H', 4, float('inf'))
                else:
                    self.updateDistribution(self.partnerDistribution, 'S', 0, 4)       
                    self.updateDistribution(self.partnerDistribution, 'H', 0, 4)     
            # jacoby convention has no semantic meaning
        elif self.biddingCategory == 'strong':
            if self.getBid(self.position, 1, bids).trump == 'D':
                if rebid.trump == 'NT':
                    self.partnerPoints = self.updatePoints(self.partnerPoints, 22, 24)
                    self.biddingCategory = 'NT'
                else:
                    self.forcing = Bid(3, rebid.trump) # refers to how high you need to go to before passing
        elif self.biddingCategory == 'weak':
            if rebid.trump == response.trump:
                self.partnerPoints = self.updatePoints(self.partnerPoints, 5, 8)
            else:
                self.partnerPoints = self.updatePoints(self.partnerPoints, 9, 11)
        else: # biddingCategory == 'normal'
            minimumRange = lambda self: self.updatePoints(self.partnerPoints, 12, 14)
            mediumRange = lambda self: self.updatePoints(self.partnerPoints, 15, 17)
            maximumRange = lambda self: self.updatePoints(self.partnerPoints, 18, 21)
            suitOrder = ['NT', 'S', 'H', 'D', 'C']
            # the minimum bid possible in suit bidded by opener
            minimumBid = self.getMinimumBidInSuit(rebid.trump, bids[:-2])
            if rebid.trump == 'NT':
                if rebid.contract == response.contract:
                    self.partnerPoints = minimumRange(self)
                else:
                    self.partnerPoints = maximumRange(self)
            # rebid opening or responding suit
            elif (rebid.trump == opening.trump or rebid.trump == response.trump):

                if rebid == minimumBid:
                   self.partnerPoints = minimumRange(self)
                elif rebid == Bid(minimumBid.contract + 1, rebid.trump):
                    self.partnerPoints = mediumRange(self)
                else:
                    self.partnerPoints = maximumRange(self)
                self.updateDistribution(self.partnerDistribution, rebid.trump, 4, 13)
            # rebid new suit
            else:
                if rebid == minimumBid: 
                    # if newsuit was reverse
                    if suitOrder.index(response.trump) < suitOrder.index(opening.trump):
                        self.partnerPoints = self.updatePoints(self.partnerPoints, 15, 17)
                    # no reversal
                    else:
                        self.partnerPoints = self.updatePoints(self.partnerPoints, 12, 17)
                else:
                    self.partnerPoints = self.updatePoints(self.partnerPoints, 18, 21)
                self.updateDistribution(self.partnerDistribution, rebid.trump, 4, 13)


    def getMinimumBidInSuit(self, suit, bids=None):
        bids = self.bids
        maxBid = self.getLastBid(bids)
        for contract in range(1, 7):
            if maxBid < Bid(contract, suit):
                return Bid(contract, suit)

    # # returns the last
    # def getMaxBid(self, bids):
    #     for _, bid in bids[::-1]:
    #         if isinstance(bid, Bid):
    #             return bid

    def interpretPartnerFirstBid(self, bids):
        self.getBidCategory()
        partnerFirstBid = self.getBid(self.partner, 1, bids)
        # 'NT', 'strong', 'weak', and  'normal'
        if self.biddingCategory == 'NT':
            for suit in self.partnerDistribution:
                self.updateDistribution(self.partnerDistribution, suit, 2, 5)
            NTPoints = {
                1: (15, 17),
                2: (20, 21),
                3: (25, 27)
            }
            self.partnerPoints = NTPoints[partnerFirstBid.contract]
        elif self.biddingCategory == 'strong':
            self.partnerPoints = self.updatePoints(self.partnerPoints, 21, float('inf'))
        elif self.biddingCategory == 'weak':
            self.partnerPoints = self.updatePoints(self.partnerPoints, 5, 11)
        else: # biddingCategory == 'normal'
            self.partnerPoints = self.updatePoints(self.partnerPoints, 12, 20)
            if partnerFirstBid.trump in 'SH':
                self.updateDistribution(self.partnerDistribution, partnerFirstBid.trump, 5, float('inf'))
            elif partnerFirstBid.trump == 'D':
                self.updateDistribution(self.partnerDistribution, partnerFirstBid.trump, 4, float('inf'))
            else: # trump is clubs
                self.updateDistribution(self.partnerDistribution, partnerFirstBid.trump, 2, float('inf'))
        

    # returns 'NT', 'strong', 'weak', and  'normal' based on firstBid
    def getBidCategory(self):
        firstBid = self.firstBid(self.bids)[1]
        if firstBid.trump == 'NT':
            self.biddingCategory = 'NT'
        elif firstBid.contract == 2:
            if firstBid.trump == 'C':
                self.biddingCategory = 'strong'
            else:
                self.biddingCategory = 'weak'
        else:
            self.biddingCategory = 'normal'

    # returns an opening bid
    def getOpeningBid(self):
        if self.points < 12:
            # either opens weak 2 or passes for when points less than 12
            return self.weakOpening()
        elif self.isEvenDistribution() and self.noTrumpOpening(): 
            # noTrump opening returns False if outside of points range
            return self.noTrumpOpening()
        elif 12 < self.points < 21:
            return self.normalOpening()
        else:
            # strong conventional bid
            return Bid(2,'C')

    def normalOpening(self):
        if self.distribution['S'] >= 5 or self.distribution['H'] >= 5:
            return Bid(1, self.longerMajor())
        elif self.distribution['D'] >= 4:
            return Bid(1, 'D') # 4+ diamonds
        else:
            return Bid(1, 'C') # 2+ clubs

    # returns the longer major suit
    def longerMajor(self):
        spadesLength = self.distribution['S']
        heartsLength = self.distribution['H']
        # returns spades if hearts length == spades length (as per SAYC system booklet)
        return ['S', 'H'][int(heartsLength > spadesLength)] 


    # returns NT opening in given ranges, returns False if it falls outside range
    def noTrumpOpening(self):
        if 15 <= self.points <= 17:
            return Bid(1,'NT')
        if 20 <= self.points <= 21:
            return Bid(2,'NT')
        if 25 <= self.points <= 27:
            return Bid(3,'NT')
        return False 

    # opening bid where points are less than 12
    def weakOpening(self):
        if self.points < 5 or self.points > 11: # self.points > 11 not necessary, but robustness
            return SpecialBid('Pass')
        for suit in self.distribution:
            if self.distribution[suit] > 5 and suit != 'C':
                return Bid(2, suit) # I'm going to ignore the very unlikely scenario where there are more than 1 6+ card suits
        return SpecialBid('Pass')

    # returns True if distribution is even (i.e. 5332, 4333, or 4432)
    def isEvenDistribution(self):
        for suit in self.distribution:
            if self.distribution[suit] > 5 or self.distribution[suit] < 2:
                return False
        return True

    # returns True if bids does not contain a Bid (only passes)
    def hasNoBids(self, bids):
        for _, bid in bids:
            if isinstance(bid, Bid): #specialBids have superclass button, not Bid
                return False
        return True

    # returns the position of the first bidder 
    # (returns None if no bids, but shouldn't occur here)
    def firstBid(self, bids):
        for position, bid in bids:
            if isinstance(bid, Bid):
                return position, bid
        
    # getting points via the standard A=4, K=3, Q=2, J=1 evaluation system
    def getHandPoints(self):
        points = 0
        for card in self.hand:
            if card.number > 10:
                points += card.number - 10
        return points



###################################################################
# playing

    # actions to perform when the board is started
    def startPlay(self, hand):
        print('startPlay')
        self.hand = copy.deepcopy(hand)
        self.knownCards.update(self.hand)

    # simulate new Monte Carlo hands and returns chosen card     
    def playTurn(self, currentRound, nsTricks, ewTricks, hands):
        # if bot is in cheating mode
        if self.cheater:
            self.node = Node(hands, self.depth, self.position, currentRound, nsTricks, ewTricks, self.bid)
            self.node.calculateMinimax(True, baseHeuristic)
            return self.node.getPlay() 
        self.possibleNodes = []
        self.simulate(currentRound, nsTricks, ewTricks)
        cardPicked = self.getCard()
        self.hand.remove(cardPicked)
        return cardPicked

    # updates set of known cards
    def updateKnownCards(self, position, card):
        self.knownCards.add(card)
        if position == self.dummy:
            self.dummyHand.remove(card)

    # gives the bot the information about the dummy
    def assignDummyHand(self, hand, dealer):
        self.dummy = self.getPartner(dealer)
        self.dummyHand = hand
        self.knownCards.append(hand)

    # generates Monte Carlo that fits known information
    def simulate(self, currentRound, nsTricks, ewTricks):
        for _ in range(self.breadth):
            self.generateMonteCarlo(currentRound, nsTricks, ewTricks)

    # aggregates the cards from each node to get the modal card choice
    def getCard(self):
        # gets a dict of card mapped to number of times picked
        print(f'self.hand: {self.hand}')
        cardCount = {'base': 0}
        print(f'self.hand length in Node: {len(self.possibleNodes[0].hands[self.position])}')
        for node in self.possibleNodes:
            node.calculateMinimax(self.position in 'ns', baseHeuristic)
            proposedPlay = node.getPlay()
            value = cardCount.get(proposedPlay, 0)
            cardCount[proposedPlay] = value + 1

        # get the modal card picked
        cardPick = 'base'
        for card in cardCount: #TODO: this feels so ugly
            if cardCount[card] > cardCount[cardPick]:
                cardPick = card
        print(f'card pick: {cardPick}')

        return cardPick
               
    # appends a new MonteCarlo-ed node to possibleNodes
    def generateMonteCarlo(self, currentRound, nsTricks, ewTricks):
        montyHands = dict()
        montyHands[self.position] = self.hand
        montyHands[self.dummy] = self.dummyHand
        otherCards = self.makeUnkownDeck() # deck with known cards removed
        cardsPerPlayer = len(otherCards)//4 + 1
        if currentRound != []:
            leader = currentRound[0][0]
        else: leader = self.position

        # in case there is an uneven number of cards
        # orders so the cards are dealth in the right order
        dealOrder = 'nesw'['nesw'.index(leader):] + 'nesw'[:'nesw'.index(leader)]
        
        for direction in dealOrder:
            if direction != self.position and direction != self.dummy:
                montyHands[direction] = []
                for _ in range(cardsPerPlayer):
                    if otherCards == []: break
                    dealtCard = random.choice(otherCards) 
                    distribution = self.getDistribution(montyHands[direction])
                    montyHands[direction].append(dealtCard)
                    
                    # so the partner's distribution conforms to the information given
                    while (direction == self.partner and
                        distribution[dealtCard.suit] >= self.partnerDistribution[dealtCard.suit][1]):
                        montyHands[direction].remove(dealtCard)
                        dealtCard = random.choice(otherCards)
                        montyHands[direction].append(dealtCard)

                    otherCards.remove(dealtCard) # prevents the card from being dealt twice
        self.possibleNodes.append(Node(montyHands, self.depth, self.position, 
                                        currentRound, nsTricks, ewTricks, self.bid))

    # returns a deck with all the cards not in hand
    def makeUnkownDeck(self):
        deck = makeDeck()
        # print(f'known{self.knownCards}')
        for card in self.knownCards:
            deck.remove(card)
        return deck

###################################################################
# old/irrelevant/tbd code

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

# def makeNode(self, hands, depth, activePosition, currentRound, nsTricks, ewTricks, bid):
    #     self.node = Node(hands, depth, activePosition, currentRound, nsTricks, ewTricks, bid)

    # def botTurn(self):
    #     self.node.calculateMinimax(True, baseHeuristic)
    #     return self.node.getPlay()    
