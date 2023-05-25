'''
Created on May 5, 2023

@author: mjw
'''
from engine.Action import Action
import random
import numpy as np
from engine.Handmaid import Handmaid
from engine.Baron import Baron
from engine.Priest import Priest
from engine.Guard import Guard
from engine.Countess import Countess
from engine.King import King
from engine.Prince import Prince
from engine.Princess import Princess
import engine.util
from player.LoveLetterAI import LoveLetterAI

class QLearningAI(LoveLetterAI):
    '''
    An AI for engine testing that learns from Q table. Made for 2 player learning.
    '''

    def __init__(self, epsilon=0.1, learningRate=0.1, discountFactor=0.9):
        self.Q = {}  # Q-table
        self.epsilon = epsilon  # Exploration rate
        self.learningRate = learningRate  # Learning rate
        self.discountFactor = discountFactor  # Discount factor
        self.playerRange = 0
        self.cardsInPlay = [0, 5, 2, 2, 2, 2, 1, 1, 1]
        self.previousStates = []
        self.previousActions = []
    
    def getPossibleActions(self, hand, dealt, players):
        actions = []
        if isinstance(hand, Guard):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                target = None
            actions.append(Action(self, hand, target, engine.util.cardTypes[1]))
            actions.append(Action(self, hand, target, engine.util.cardTypes[2]))
            actions.append(Action(self, hand, target, engine.util.cardTypes[3]))
            actions.append(Action(self, hand, target, engine.util.cardTypes[4]))
            actions.append(Action(self, hand, target, engine.util.cardTypes[5]))
            actions.append(Action(self, hand, target, engine.util.cardTypes[6]))
            actions.append(Action(self, hand, target, engine.util.cardTypes[7]))
        if isinstance(dealt, Guard):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                target = None
            actions.append(Action(self, dealt, target, engine.util.cardTypes[1]))
            actions.append(Action(self, dealt, target, engine.util.cardTypes[2]))
            actions.append(Action(self, dealt, target, engine.util.cardTypes[3]))
            actions.append(Action(self, dealt, target, engine.util.cardTypes[4]))
            actions.append(Action(self, dealt, target, engine.util.cardTypes[5]))
            actions.append(Action(self, dealt, target, engine.util.cardTypes[6]))
            actions.append(Action(self, dealt, target, engine.util.cardTypes[7]))
        if isinstance(hand, Priest):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                target = None
            actions.append(Action(self, hand, target, None))
        if isinstance(dealt, Priest):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                target = None
            actions.append(Action(self, dealt, target, None))
        if isinstance(hand, Baron):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand, target, None))
            actions.append(Action(self, hand, None, None))
        if isinstance(dealt, Baron):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, dealt, target, None))
            actions.append(Action(self, dealt, None, None))
        if isinstance(hand, Handmaid):
            actions.append(Action(self, hand, self, None))
        if isinstance(dealt, Handmaid):
            actions.append(Action(self, dealt, self, None))
        if isinstance(hand, Prince):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand, target, None))
            actions.append(Action(self, hand, self, None))
            actions.append(Action(self, hand, None, None))
        if isinstance(dealt, Prince):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, dealt, target, None))
            actions.append(Action(self, dealt, self, None))
            actions.append(Action(self, dealt, None, None))
        if isinstance(hand, King):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand, target, None))
            actions.append(Action(self, hand, None, None))
        if isinstance(dealt, King):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, dealt, target, None))
            actions.append(Action(self, dealt, None, None))
        if isinstance(hand, Countess):
            actions.append(Action(self, hand, None, None))
        if isinstance(dealt, Countess):
            actions.append(Action(self, dealt, None, None))
        
        return actions


    def getQValue(self, state, action):
        # Retrieve the Q-value for the given state-action pair
        return self.Q.get((state, action), 0.0)
    
    def updateQValue(self, state, action, futureReward):
        # Update the Q-value for the given state-action pair based on the new state and reward
        old_q = self.getQValue(state, action)
        new_q = (1 - self.learning_rate) * old_q + self.learning_rate * (self.discount_factor * futureReward)
        self.Q[(state, action)] = new_q
    
    def chooseAction(self, state, hand, dealt, players):
        # exploration vs exploitation
        if random.uniform(0, 1) < self.epsilon:
            # explore: choose a random action
            action = random.choice((hand, dealt))
        else:
            actions = self.getPossibleActions(hand, dealt, players)
                
            # exploit: choose the action with the highest Q-value for the current state
            q_values = [self.getQValue(state, action) for action in actions]
            max_q = max(q_values)
            best_actions = [action for action, q_value in zip(actions, q_values) if q_value == max_q]
            action = random.choice(best_actions)
        return action

    def getAction(self, dealtCard, deckSize, graveState, players):

        # If we have to play the countess
        if isinstance(self.hand, Countess) and (isinstance(dealtCard, King) or isinstance(dealtCard, Prince)) :
            return Action(self, self.hand, self, None)
        elif isinstance(dealtCard, Countess) and (isinstance(self.hand, King) or isinstance(self.hand, Prince)) :
            return Action(self, dealtCard, self, None)

        self.pruneAction(dealtCard)
        hand = [self.hand, dealtCard]
        state = [hand, self.playerRange, deckSize, players]

        choice = self.chooseAction(state, hand, dealtCard, players)
        self.previousStates.append(state)
        self.previousActions.append(choice)

        return choice

    
    def pruneAction(self, drawnCard):
        if isinstance(drawnCard, Guard):
            self.cardsInPlay[1] -= 1
            if self.cardsInPlay[1] <= 0:
                self.playerRange.remove(1)
        if isinstance(drawnCard, Priest):
            self.cardsInPlay[2] -= 1
            if self.cardsInPlay[2] <= 0:
                self.playerRange.remove(2)
        if isinstance(drawnCard, Baron):
            self.cardsInPlay[3] -= 1
            if self.cardsInPlay[3] <= 0:
                self.playerRange.remove(3)
        if isinstance(drawnCard, Handmaid):
            self.cardsInPlay[4] -= 1
            if self.cardsInPlay[4] <= 0:
                self.playerRange.remove(4)
        if isinstance(drawnCard, Prince):
            self.cardsInPlay[5] -= 1
            if self.cardsInPlay[5] <= 0:
                self.playerRange.remove(5)
        if isinstance(drawnCard, King):
            self.cardsInPlay[6] -= 1
            if self.cardsInPlay[6] <= 0:
                self.playerRange.remove(6)
        if isinstance(drawnCard, Countess):
            self.cardsInPlay[7] -= 1
            if self.cardsInPlay[7] <= 0:
                self.playerRange.remove(7)
        if isinstance(drawnCard, Princess):
            self.cardsInPlay[8] -= 1
            if self.cardsInPlay[8] <= 0:
                self.playerRange.remove(8)

    def notifyOfAction(self, action, graveState):
        self.cardsInPlay[action.playedCard.value] -= 1

        self.pruneRanges(action, graveState)
    
    def priestKnowledge(self, player, card):
        self.playerRange = card.value

    def pruneRanges(self, action, graveState):
        # if discarded card is in player range - reset range
        # if the card played was one we were tracking, we now have to reset 
        # our guess
        if action.playedCard.value in self.playerRange:
            self.playerRange = [1, 2, 3, 4, 5, 6, 7, 8]

        # updates player range based on cardsInPlay
        for cardType in range(1, 9):
            if self.cardsInPlay[cardType] == 0 and cardType in self.playerRange:
                # just in case it's wrong
                self.playerRange.remove(cardType)

        # TODO: track what happens now that the engine notifies of elimination
        if isinstance(action.playedCard, Baron):
            # Action of discarding after comparing cards
            # in the very small chance that it's the beginning of the game
            if len(graveState) >= 2:
                loserAction = graveState[len(graveState) - 2]
                lower = loserAction.playedCard.value
                if action.doer == loserAction.doer:
                    self.playerRange = list(range(lower + 1, 9))
                else:
                    self.playerRange = list(range(lower + 1, 9))

        elif isinstance(action.playedCard, Guard):
            # Just in case the bot is wrong
            if action.target != self and action.guess.value in self.playerRange:
                # if the guess was something we thought that player had,
                # and the player said he doesn't have it
                # remove it from what we were tracking
                self.playerRange.remove(action.guess.value)
    
    def notifyEliminate(self, player):
        if player.equals(self):
            if len(self.previousStates) >= 1:
                prevStates = self.previousStates[::-1]
                prevActions = self.previousActions[::-1]
                for i in range(len(prevStates)):
                    self.updateQValue(prevStates[i], prevActions[i], -1/(i+1))
            self.playerRange = 0
            self.cardsInPlay = [0, 5, 2, 2, 2, 2, 1, 1, 1]
            self.previousStates = []
            self.previousActions = []
        else:
            if len(self.previousStates) >= 1:
                prevStates = self.previousStates[::-1]
                prevActions = self.previousActions[::-1]
                for i in range(len(prevStates)):
                    self.updateQValue(prevStates[i], prevActions[i], 1/(i+1))
            self.playerRange = 0
            self.cardsInPlay = [0, 5, 2, 2, 2, 2, 1, 1, 1]
            self.previousStates = []
            self.previousActions = []
    
    def __str__(self):
        return "QLearningAI"+str(self.number)