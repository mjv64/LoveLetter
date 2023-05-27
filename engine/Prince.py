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

    person = "Prince"
    value = 5

    def perform(self, action, players, engine, deck):
        # discard player's hand
        if action.target is not None:
            engine.abnormalDiscard(action.target, action.target.hand)
