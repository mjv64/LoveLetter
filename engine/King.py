'''
Created on Nov 26, 2016

@author: mjw
'''
from engine.Card import Card

class King(Card):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.person = "King"
        self.value = 6

    def perform(self, action, players, engine, deck):
        # swap hands
        doerHand = action.doer.hand
        targetHand = action.target.hand
        action.target.hand = doerHand
        action.doer.hand = targetHand
    
    # Value of playing this card is the value of the card kept in hand.
    # Same as handmaid, priest, prince
    def getHeuristic(self, bot, otherCard, players):
        return [otherCard.value, bot.chooseRandom(players), None]
        # TODO: Implement with Time interval and range checker