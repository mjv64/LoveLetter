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
        # select player
        # swap hands
        doerHand = action.doer.hand
        targetHand = action.target.hand
        action.target.hand = doerHand
        action.doer.hand = targetHand

    def getHeuristic(self, bot, otherCard):
        return [otherCard.value, bot.chooseRandom(), None]
        # TODO: Implement with Time interval and range checker