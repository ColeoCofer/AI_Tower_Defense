import pygame
import random
import sys
import numpy as np

from constants.aiConstants import *
from constants.gameConstants import *
from agent.qLearningAgent import QLearningAgent
from game.game import Game


class QLearning:

    def __init__(self, agent):  
        self.agent        = agent
        self.epsilon      = EPSILON

        self.trainingMode = False
        self.visualMode   = True

        # Array of position indexes to track which locations have a tower placed there. -1 for empty position, and tower type index otherwise
        self.towerPlacements = [-1] * STARTING_POSITIONS

    '''
    Current workflow concept:
        Initialize a qLearningAgent that views the qLearning process at a high level
            For each game, create a Qlearning object to handle the game level details
                while(game not over)
                    chooseAction()
                    performAction()
                applyRewardToEachTowerPlacement() (in qTable)
    '''

    '''
    TODO
    Find out how to rewrite run()
    Figure out how we want to place  towers
    Decide what is handled by this file vs the agent file
    Figure out testing procedures / make sure the code is logical
    '''

    def run(self):
        self.agent.initTowers()  # Do we want to place towers in this file instead?
       
        for N in range(N_EPISODES):
            # decrease epsilon every 50 episodes
            if self.epsilon >= 0 and self.trainingMode == ON:
                if N % EPSILON_PERIOD == 0:
                    self.epsilon -= EPSILON_STEP

            # Should be while game not over
            for M in range(M_STEPS):
            # Robby makes a move using epsilon-greedy
            # robby, reward = nextAction(epsilon, Qmatrix, robby, board, actionTax)
            # # Update the Q-matrix after each action
            # if trainingModeOn:
            #     Qmatrix = updateQmatrix(eta, gamma, Qmatrix, robby, reward, robbiesOldState, robbiesOldPosition)


            # bool: visualMode, bool: trainingMode, Agent: agent
                game = Game(self.visualMode, self.trainingMode, self.agent)
                game.run()
        return

    def chooseAction(self):
        """ Chooses the next best tower and location to place """

        if random.random() < self.epsilon:
            #Pick randomly
            location = random.randrange(0, STARTING_POSITIONS, 1)
            tower = random.randrange(0, NUMBER_OF_TOWERS, 1)
            while not self.checkLegal(location):
                location = random.randrange(0, STARTING_POSITIONS, 1)

            return (location, tower)
        else:
            #Greedily pick using Q-table
            bestQValueIndices = [(0, 0)]
            for location in range(STARTING_POSITIONS):
                for tower in range(NUMBER_OF_TOWERS):
                    #Finds the best tower for a single location in the tower grid
                    if self.agent.qtable[location][tower] > self.agent.qtable[bestQValueIndices[0][0]][bestQValueIndices[0][1]]:
                        bestQValueIndices.clear()
                        bestQValueIndices.append((location, tower))
                    elif self.agent.qtable[location][tower] == self.agent.qtable[bestQValueIndices[0][0]][bestQValueIndices[0][1]]:
                        bestQValueIndices.append((location, tower))

        return random.choice(bestQValueIndices)

    def findHighestQValue(self):
        return np.amax(self.agent.qtable)

    def checkLegal(self, placementIndex):
        if self.towerPlacements[placementIndex] == 0:
            return True
        else:
            return False

    def applyReward(self, score):
        for i in range(len(self.towerPlacements)):
            if self.towerPlacements[i] is not -1:
                self.updateQtable(self.towerPlacements[i], i, score)

    def updateQtable(self, tower, placement, score):
        self.agent.qtable[tower][placement] = \
            self.agent.qtable[tower][placement] + LEARN_RATE * \
            (score + DISCOUNT_RATE * self.findHighestQValue() - self.agent.qtable[tower][placement])
