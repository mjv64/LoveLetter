'''
Created on Nov 26, 2016

@author: mjw
'''
from engine.Card import Card
from engine.Action import Action

class Prince(Card):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.person = "Prince"
        self.value = 5

    def perform(self, action, players, engine, deck):
        # choose player to discard hand
        # discard player's hand
        # force a redraw
        # discard card
        engine.discard(action.target, action.target.hand)
        action.target.hand = deck.getCard()

    def getHeuristic(self, bot, otherCard):
        return [otherCard.value, bot.chooseRandom(), None]