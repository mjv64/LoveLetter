'''
Created on Nov 26, 2016

@author: mjw
'''
from engine.Card import Card

class Priest(Card):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.person = "Priest"
        self.value = 2

    def perform(self, action, players, engine, deck):
        # reveal another player's hand
        # add to knowledge base?
        action.doer.priestKnowledge(action.target, action.target.hand)

    def getHeuristic(self, bot, otherCard):
        return [otherCard.value, bot.chooseRandom(), None]