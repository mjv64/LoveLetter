'''
Created on Dec 5, 2016

@author: mjw
'''

from engine.Card import Card
import random

class DebugCard(Card):
    '''
    A card that eliminates an opposing player unconditionally
    '''
    
    value = 99

    def __init__(self):
        '''
        Constructor
        '''
    
    def perform(self, action, players, grave, deck):
        eliminated = action.doer
        while eliminated is action.doer:
            eliminated = random.choice(players)
        grave.append(eliminated.hand)
        players.remove(eliminated)