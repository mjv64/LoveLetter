'''
Created on Nov 26, 2016

@author: mjw
'''
from engine.Card import Card

class Prince(Card):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        person = "Prince"
        value = 5

    def perform(self, action, players, grave, deck):
    	# choose player to discard hand
    	# discard player's hand
    	# force a redraw
    	# discard card
        grave.append(Action(None, action.target.hand, None, None))
        action.target.hand = deck.getCard()
        