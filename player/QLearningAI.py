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
        self.playerRange = [1, 2, 3, 4, 5, 6, 7, 8]
        self.cardsInPlay = [0, 5, 2, 2, 2, 2, 1, 1, 1]
        self.previousStates = []
        self.previousActions = []
    
    def getQAction(self, action):
        Qaction = None
        if action.target == None:
            Qaction = [type(action.playedCard), 0, action.guess]
        else:
            if action.target == action.doer:
                Qaction = [type(action.playedCard), 1, action.guess]
            else:
                Qaction = [type(action.playedCard), 2, action.guess]
        return Qaction
    
    def decodeQAction(self, Qaction, hand, players):
        other_players = [player for player in players if player is not self]
        action = None
        card = None
        if isinstance(hand[0], Qaction[0]):
            card = hand[0]
        if isinstance(hand[1], Qaction[0]):
            card = hand[1]
        if Qaction[1] == 0:
            action = Action(self, card, None, Qaction[2])
        else:
            if Qaction[1] == 1:
                action = Action(self, card, self, Qaction[2])
            else:
                action = Action(self, card, other_players[0], Qaction[2])
        return action
    
    def getQState(self, state):
        Qstate = []
        for card in state[0]:
            if card == None:
                Qstate.append(None)
            else:
                Qstate.append(type(card))
        Qstate.append(state[1])
        if state[2] <= 7:
            Qstate.append(True)
        else:
            Qstate.append(False)
        return Qstate

    def getPossibleActions(self, hand, players):
        actions = []
        if isinstance(hand[0], Guard):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                target = None
            actions.append(Action(self, hand[0], target, engine.util.cardTypes[1]))
            actions.append(Action(self, hand[0], target, engine.util.cardTypes[2]))
            actions.append(Action(self, hand[0], target, engine.util.cardTypes[3]))
            actions.append(Action(self, hand[0], target, engine.util.cardTypes[4]))
            actions.append(Action(self, hand[0], target, engine.util.cardTypes[5]))
            actions.append(Action(self, hand[0], target, engine.util.cardTypes[6]))
            actions.append(Action(self, hand[0], target, engine.util.cardTypes[7]))
        if isinstance(hand[1], Guard):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                target = None
            actions.append(Action(self, hand[1], target, engine.util.cardTypes[1]))
            actions.append(Action(self, hand[1], target, engine.util.cardTypes[2]))
            actions.append(Action(self, hand[1], target, engine.util.cardTypes[3]))
            actions.append(Action(self, hand[1], target, engine.util.cardTypes[4]))
            actions.append(Action(self, hand[1], target, engine.util.cardTypes[5]))
            actions.append(Action(self, hand[1], target, engine.util.cardTypes[6]))
            actions.append(Action(self, hand[1], target, engine.util.cardTypes[7]))
        if isinstance(hand[0], Priest):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                target = None
            actions.append(Action(self, hand[0], target, None))
        if isinstance(hand[1], Priest):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
            else:
                target = None
            actions.append(Action(self, hand[1], target, None))
        if isinstance(hand[0], Baron):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand[0], target, None))
            actions.append(Action(self, hand[0], None, None))
        if isinstance(hand[1], Baron):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand[1], target, None))
            actions.append(Action(self, hand[1], None, None))
        if isinstance(hand[0], Handmaid):
            actions.append(Action(self, hand[0], self, None))
        if isinstance(hand[1], Handmaid):
            actions.append(Action(self, hand[1], self, None))
        if isinstance(hand[0], Prince):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand[0], target, None))
            actions.append(Action(self, hand[0], self, None))
            actions.append(Action(self, hand[0], None, None))
        if isinstance(hand[1], Prince):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand[1], target, None))
            actions.append(Action(self, hand[1], self, None))
            actions.append(Action(self, hand[1], None, None))
        if isinstance(hand[0], King):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand[0], target, None))
            actions.append(Action(self, hand[0], None, None))
        if isinstance(hand[1], King):
            other_players = [player for player in players if player is not self]
            if other_players:
                target = random.choice(other_players)
                actions.append(Action(self, hand[1], target, None))
            actions.append(Action(self, hand[1], None, None))
        if isinstance(hand[0], Countess):
            actions.append(Action(self, hand[0], None, None))
        if isinstance(hand[1], Countess):
            actions.append(Action(self, hand[1], None, None))
        
        return actions
    
    def convert_to_hashable(self, thing):
        if isinstance(thing, list):
            return tuple(self.convert_to_hashable(item) for item in thing)
        else:
            return thing
    
    def getQValue(self, state, action):
        # Retrieve the Q-value for the given state-action pair
        return self.Q.get((self.convert_to_hashable(state), self.convert_to_hashable(action)), 0.0)
    
    def updateQValue(self, state, action, futureReward):
        # Update the Q-value for the given state-action pair based on the new state and reward
        old_q = self.getQValue(state, action)
        new_q = (1 - self.learningRate) * old_q + self.learningRate * (self.discountFactor * futureReward)
        self.Q[(self.convert_to_hashable(state), self.convert_to_hashable(action))] = new_q
    
    def chooseAction(self, state, hand, players):
        # exploration vs exploitation
        if random.uniform(0, 1) < self.epsilon:
            # explore: choose a random action
            action = random.choice(self.getPossibleActions(hand, players))
        else:
            actions = self.getPossibleActions(hand, players)
            Qactions = [self.getQAction(action) for action in actions]
            Qstate = self.getQState(state)
                
            # exploit: choose the action with the highest Q-value for the current state
            q_values = [self.getQValue(Qstate, Qaction) for Qaction in Qactions]
            if q_values:
                max_q = max(q_values)
                best_actions = [self.decodeQAction(action, hand, players) for action, q_value in zip(Qactions, q_values) if q_value == max_q]
                action = random.choice(best_actions)
            else:
                action = random.choice(self.getPossibleActions(hand, players))
        return action

    def getAction(self, dealtCard, deckSize, graveState, players):

        # If we have to play the countess
        if isinstance(self.hand, Countess) and (isinstance(dealtCard, King) or isinstance(dealtCard, Prince)) :
            return Action(self, self.hand, self, None)
        elif isinstance(dealtCard, Countess) and (isinstance(self.hand, King) or isinstance(self.hand, Prince)) :
            return Action(self, dealtCard, self, None)

        self.pruneAction(dealtCard)
        hand = [self.hand, dealtCard]
        state = [hand, self.playerRange, deckSize]

        choice = self.chooseAction(state, hand, players)
        self.previousStates.append(self.getQState(state))
        self.previousActions.append(self.getQAction(choice))

        return choice

    
    def pruneAction(self, drawnCard):
        if isinstance(drawnCard, Guard):
            self.cardsInPlay[1] -= 1
            if self.cardsInPlay[1] <= 0 and 1 in self.playerRange:
                self.playerRange.remove(1)
        if isinstance(drawnCard, Priest):
            self.cardsInPlay[2] -= 1
            if self.cardsInPlay[2] <= 0 and 2 in self.playerRange:
                self.playerRange.remove(2)
        if isinstance(drawnCard, Baron):
            self.cardsInPlay[3] -= 1
            if self.cardsInPlay[3] <= 0 and 3 in self.playerRange:
                self.playerRange.remove(3)
        if isinstance(drawnCard, Handmaid):
            self.cardsInPlay[4] -= 1
            if self.cardsInPlay[4] <= 0 and 4 in self.playerRange:
                self.playerRange.remove(4)
        if isinstance(drawnCard, Prince):
            self.cardsInPlay[5] -= 1
            if self.cardsInPlay[5] <= 0 and 5 in self.playerRange:
                self.playerRange.remove(5)
        if isinstance(drawnCard, King):
            self.cardsInPlay[6] -= 1
            if self.cardsInPlay[6] <= 0 and 6 in self.playerRange:
                self.playerRange.remove(6)
        if isinstance(drawnCard, Countess):
            self.cardsInPlay[7] -= 1
            if self.cardsInPlay[7] <= 0 and 7 in self.playerRange:
                self.playerRange.remove(7)
        if isinstance(drawnCard, Princess):
            self.cardsInPlay[8] -= 1
            if self.cardsInPlay[8] <= 0 and 8 in self.playerRange:
                self.playerRange.remove(8)

    def notifyOfAction(self, action, graveState):
        self.cardsInPlay[action.playedCard.value] -= 1

        self.pruneRanges(action, graveState)
    
    def priestKnowledge(self, player, card):
        self.playerRange = [card.value]

    def pruneRanges(self, action, graveState):
        # if discarded card is in player range - reset range
        # if the card played was one we were tracking, we now have to reset 
        # our guess
        self.playerRange = [1, 2, 3, 4, 5, 6, 7, 8]

        # updates player range based on cardsInPlay
        for cardType in range(1, 9):
            if self.cardsInPlay[cardType] == 0 and cardType in self.playerRange:
                # just in case it's wrong
                self.playerRange.remove(cardType)
    
    def notifyEliminate(self, player):
        if player == self:
            if len(self.previousStates) >= 1:
                prevStates = self.previousStates[::-1]
                prevActions = self.previousActions[::-1]
                for i in range(len(prevStates)):
                    self.updateQValue(prevStates[i], prevActions[i], -1/(i+1))
            self.playerRange = 0
            self.cardsInPlay = [0, 5, 2, 2, 2, 2, 1, 1, 1]
            self.playerRange = [1, 2, 3, 4, 5, 6, 7, 8]
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
            self.playerRange = [1, 2, 3, 4, 5, 6, 7, 8]
            self.previousStates = []
            self.previousActions = []
    
    def getQTable(self):
        return self.Q
    def __str__(self):
        return "QLearningAI"