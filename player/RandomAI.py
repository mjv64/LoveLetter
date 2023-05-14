'''
Created on Nov 27, 2016

@author: mjw
'''
from engine.Action import Action
import random
from engine.Handmaid import Handmaid
from engine.Countess import Countess
from engine.King import King
from engine.Prince import Prince
import engine.util
from player.LoveLetterAI import LoveLetterAI

class RandomAI(LoveLetterAI):
    '''
    An AI for engine testing that makes a random choice for all actions.
    
    Alternately, it is an AI that always takes a random choice.
    '''
    
    numBots = 0

    def __init__(self):
        self.number = RandomAI.numBots
        RandomAI.numBots+=1
    
    def getAction(self, dealtCard, deckSize, graveState, players):
        # ok it's not totally random, but let's not have the bot be a total fool
        # and just play the handmaid on someone else
        choice = random.choice((self.hand, dealtCard))
        target = self

        # If we have to play the countess
        if isinstance(self.hand, Countess) and (isinstance(dealtCard, King) or isinstance(dealtCard, Prince)) :
            return Action(self, self.hand, self, None)
        elif isinstance(dealtCard, Countess) and (isinstance(self.hand, King) or isinstance(self.hand, Prince)) :
            return Action(self, dealtCard, self, None)

        if not isinstance(choice, Handmaid):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                # Other players are handmaiden'd up and can't be targeted
                
                # Only Prince is self-targeted, according to the rulebook in this 
                # special instance where all other players are handmaiden'd up
                if isinstance(choice, Prince):
                    return Action(self, choice, self, None)
                # Otherwise, set target to None and use custom logic 
                # on other cards' perform functions, to ignore None target Actions
                else:
                    target = None
            
        classIndex = random.randrange(1,len(engine.util.cardTypes))
        return Action(self, choice, target, engine.util.cardTypes[classIndex])
    
    def notifyOfAction(self, action, graveState):
        pass
    
    def priestKnowledge(self, player, card):
        pass
    
    def notifyEliminate(self, player):
        pass
    
    def __str__(self):
        return "RandomAI"+str(self.number)