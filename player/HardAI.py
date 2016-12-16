'''
Created on Dec 5, 2016

Hard AI player

@author: Ben, Patrick, Josh
'''
from engine.Countess import Countess
from engine.Baron import Baron
from engine.Guard import Guard
from engine.Handmaid import Handmaid
from engine.King import King
from engine.Priest import Priest
from engine.Prince import Prince
from engine.Princess import Princess

from .Player import Player
from random import choice
from engine.Action import Action

import engine.util


class HardAI(Player):
    '''
    An AI that monitors other players' actions and the state of the graveyard
    to make its action decisions. The AI has two different playstyles: Aggressive
    and Defensive, that help it make more informed decisions.
    '''

    numBots = 0

    def __init__(self, playstyle, isAggressive):
        # index == value of card (1-indexed)
        self.number = HardAI.numBots
        HardAI.numBots += 1
        self.cardsInPlay = [0, 5, 2, 2, 2, 2, 1, 1, 1]
        self.playerRanges = {}
        self.isAggressive = isAggressive
        self.priestKnown = None
        
    def notifyEliminate(self, player):
        if player != self:
            self.playerRanges.pop(player)
        
    def assignHand(self, card, players):
        Player.assignHand(self, card, players)
        # initialize players on first turn
        for player in players:
            if player != self:
                self.playerRanges[player] = [1,2,3,4,5,6,7,8]

    # calculates a heuristic for both cards and plays the card with the 
    # lower estimated value to improve it's own value
    # Note: some cards's heuristics are really the other cards' values.
    # This might invert the logic
    def getAction(self, dealtCard, deckSize, graveState, players):
        card1 = self.hand
        card2 = dealtCard

        classes = engine.util.cardTypes

        # Princess Force Move
        if isinstance(card1, Princess):
            param = card2.getHeuristic(self, card1, players)
            return Action(self, card2, param[1], classes[param[2]-1] if param[2] != None else None)
        elif isinstance(card2, Princess):
            param = card1.getHeuristic(self, card2, players)
            return Action(self, card1, param[1], classes[param[2]-1] if param[2] != None else None)

        # Countess Force Move
        if isinstance(card1, Countess):
            if isinstance(card2, King) or isinstance(card2, Prince):
                return Action(self, card1, None, None)
        elif isinstance(card2, Countess):
            if isinstance(card1, King) or isinstance(card1, Prince):
                return Action(self, card2, None, None)

        # Check Heuristics
        card1Heuristic = card1.getHeuristic(self, card2, players)
        card2Heuristic = card2.getHeuristic(self, card1, players)

        # Play (get rid of) the card with the lowest estimated value
        if(card1Heuristic[0] > card2Heuristic[0]):
            return Action(self, card2, card2Heuristic[1], classes[card2Heuristic[2]-1] if card2Heuristic[2] != None else None)
        else:
            return Action(self, card1, card1Heuristic[1], classes[card1Heuristic[2]-1] if card1Heuristic[2] != None else None)
        
    def __str__(self):
        return "HardAI"+str(self.number)

    def notifyOfAction(self, action, graveState):
        # Decrement amount of cards in play
        # TODO: Account for cards in hand
        # TODO: If action.doer is you, then don't decrement
        self.cardsInPlay[action.playedCard.value] -= 1

        self.pruneRanges(action, graveState)

    # Choose a player that is not this bot
    def chooseRandom(self, players):
        player = self
        while player == self:
            player = choice(players)
        return player

    # Used with Guard
    # Find the player with the narrowest range of possible cards in hand
    def getMinRangePlayer(self):
        playerRangeLength = 10
        minPlayer= None
        for player in self.playerRanges:
            # TODO: fix logic
            if player != self:
                if len(self.playerRanges[player]) < playerRangeLength:
                    minPlayer= player
        return minPlayer

    def priestKnowledge(self, player, card):
        self.playerRanges[player] = [card.value]

    def pruneRanges(self, action, graveState):
        # if discarded card is in player range - reset range
        # if the card played was one we were tracking, we now have to reset 
        # our guess
        if action.playedCard.value in self.playerRanges[action.doer]:
            self.playerRanges[action.doer] = [1, 2, 3, 4, 5, 6, 7, 8]

        # updates player range based on cardsInPlay
        for cardType in range(1, 9):
            if self.cardsInPlay[cardType] == 0 and cardType in self.playerRanges[action.doer]:
                # just in case it's wrong
                self.playerRanges[action.doer].remove(cardType)

        # if Countess discarded, high probability of Prince, King, Princess
        if isinstance(action.playedCard, Countess):
            self.playerRanges[action.doer] = [5, 6, 8]

        # TODO: track what happens now that the engine notifies of elimination
        elif isinstance(action.playedCard, Baron):
            # Action of discarding after comparing cards
            # in the very small chance that it's the beginning of the game
            if len(graveState) >= 2:
                loserAction = graveState[len(graveState) - 2]
                lower = loserAction.playedCard.value
                if action.doer == loserAction.doer:
                    self.playerRanges[action.target] = list(range(lower + 1, 9))
                else:
                    self.playerRanges[action.doer] = list(range(lower + 1, 9))

        elif isinstance(action.playedCard, Guard):
            # Just in case the bot is wrong
            if action.target != self and action.guess.value in self.playerRanges[action.target]:
                # if the guess was something we thought that player had,
                # and the player said he doesn't have it
                # remove it from what we were tracking
                self.playerRanges[action.target].remove(action.guess.value)