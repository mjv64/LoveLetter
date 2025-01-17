'''
Created on Nov 26, 2016

@author: mjw
'''
from engine.Card import Card

class King(Card):
    '''
    classdocs
    '''
    
    person = "King"
    value = 6

    def perform(self, action, players, engine, deck):
        if not action.target:
            return # No valid target, behavior is to discard this card
        # swap hands
        doerHand = action.doer.hand
        targetHand = action.target.hand
        action.target.hand = doerHand
        action.doer.hand = targetHand
