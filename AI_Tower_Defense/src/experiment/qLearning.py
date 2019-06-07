import pygame
import random
import sys
import numpy as np

from constants.aiConstants import *
from constants.gameConstants import *
from agent.qLearningAgent import QLearningAgent
from game.game import Game


class QLearning:

    def __init__(self, visualMode):
        # self.agent        = agent
        self.epsilon      = EPSILON

        self.visualMode   = visualMode

        # Array of position indexes to track which locations have a tower placed there. -1 for empty position, and tower type index otherwise
        self.towerPlacements = [-1] * STARTING_POSITIONS
        self.qtable = np.zeros((STARTING_POSITIONS, NUMBER_OF_TOWERS))
        self.towers = []

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
    Figure out how we want to place towers
    Decide what is handled by this file vs the agent file
    Figure out testing procedures / make sure the code is logical
    '''

    def run(self):
        for N in range(1):  #N_EPISODES
            # decrease epsilon every 50 episodes
            if self.epsilon >= 0:  #  and self.trainingMode == ON:
                if N % EPSILON_PERIOD == 0:
                    self.epsilon -= EPSILON_STEP

            # Should be while game not over
            self.towers = []
            print(f"VISUAL MODE: {self.visualMode}")
            for M in range(NUMBER_OF_STARTING_TOWERS):
                # Robby makes a move using epsilon-greedy
                # robby, reward = nextAction(epsilon, Qmatrix, robby, board, actionTax)
                # # Update the Q-matrix after each action
                # if trainingModeOn:
                #     Qmatrix = updateQmatrix(eta, gamma, Qmatrix, robby, reward, robbiesOldState, robbiesOldPosition)


                # bool: visualMode, bool: trainingMode, Agent: agent
                nextAction = self.chooseAction()
                if nextAction[1] > NUMBER_OF_TOWERS - 1:
                    print(f"TowerIndex: {nextAction[1]}")
                if nextAction[0] > STARTING_POSITIONS - 1:
                    print(f"PositionIndex: {nextAction[0]}")

                towerLocation = TOWER_GRID[nextAction[0]]
                towerLocation = (towerLocation[0] + (TOWER_GRID_SIZE / 2), towerLocation[1] + (TOWER_GRID_SIZE / 2))

                newTower = TOWER_TYPES[nextAction[1]](towerLocation)
                self.towers.append(newTower)

            game = Game(self.visualMode, self.towers, None)
            game.run()
        return

    def chooseAction(self):
        """ Chooses the next best tower and location to place """

        if random.random() < self.epsilon:
            #Pick randomly
            location = random.randint(0, STARTING_POSITIONS - 1)
            tower = random.randint(0, NUMBER_OF_TOWERS - 1)
            while not self.isLegal(location):
                location = random.randint(0, STARTING_POSITIONS)

            return (location, tower)
        else:
            #Greedily pick using Q-table
            bestQValueIndices = [(0, 0)]
            for location in range(STARTING_POSITIONS):
                for tower in range(NUMBER_OF_TOWERS):
                    #Finds the best tower for a single location in the tower grid
                    if self.qtable[location][tower] > self.qtable[bestQValueIndices[0][0]][bestQValueIndices[0][1]] and self.isLegal(location):
                        bestQValueIndices.clear()
                        bestQValueIndices.append((location, tower))
                    elif self.qtable[location][tower] == self.qtable[bestQValueIndices[0][0]][bestQValueIndices[0][1]] and self.isLegal(location):
                        bestQValueIndices.append((location, tower))

        return random.choice(bestQValueIndices)

    def findHighestQValue(self):
        return np.amax(self.qtable)

    def isLegal(self, placementIndex):
        gridPosition = TOWER_GRID[placementIndex]
        gridPosition = (gridPosition[0] + (TOWER_GRID_SIZE / 2), gridPosition[1] + (TOWER_GRID_SIZE / 2))
        print(f"New Tower Position: [{gridPosition[0]}][{gridPosition[1]}]")
        for i in range(len(self.towers)):
            print(f"Current Tower Position: [{self.towers[i].position[0]}][{self.towers[i].position[1]}]")
            if gridPosition == self.towers[i].position:
                return False
        return True
        # if self.towerPlacements[placementIndex] == 0:
        #     return True
        # else:
        #     return False

    def applyReward(self, score):
        for i in range(len(self.towerPlacements)):
            if self.towerPlacements[i] is not -1:
                self.updateQtable(self.towerPlacements[i], i, score)

    def updateQtable(self, tower, placement, score):
        self.qtable[tower][placement] = \
            self.qtable[tower][placement] + LEARN_RATE * \
            (score + DISCOUNT_RATE * self.findHighestQValue() - self.qtable[tower][placement])
