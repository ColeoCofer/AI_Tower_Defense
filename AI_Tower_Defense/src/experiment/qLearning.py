import pygame
import random
import sys
import numpy as np

from constants.aiConstants import *
from constants.gameConstants import *
from agent.qLearningAgent import QLearningAgent
from game.game import Game

LOAD_QTABLE_FROM_FILE = True

class QLearning:

    def __init__(self, visualMode):
        self.epsilon    = EPSILON
        self.visualMode = visualMode

        # Array of position indices to track which locations have a tower placed there. -1 for empty position, and tower type index otherwise
        self.towerPlacements = [-1] * STARTING_POSITIONS
        self.qtable = np.zeros((STARTING_POSITIONS, NUMBER_OF_TOWERS))
        self.towers = []

    def run(self):
        ''' Kicks off multiple game instances and updates the q-table after each game ends '''

        # Read in saved qtable and continue training
        if LOAD_QTABLE_FROM_FILE:
            self.qtable = self.loadData()

        # Number of games to train on
        for N in range(10):
            # decrease epsilon every 50 episodes
            if self.epsilon >= 0:  #  and self.trainingMode == ON:
                if N % EPSILON_PERIOD == 0:
                    self.epsilon -= EPSILON_STEP

            self.towers = []
            # Each step determines the next tower to place
            for M in range(NUMBER_OF_STARTING_TOWERS):
                location, tower = self.chooseAction()
                self.addTower(location, tower)

            # Run the game until it's over
            game = Game(self.visualMode, self.towers, None)
            game.run()

            # Update q-table for each tower placement using the final game score
            self.applyReward(game.score)
            self.saveData()

        return

    def addTower(self, location, tower):
        ''' Adds a new tower into the list of starting towers '''
        self.towerPlacements[location] = tower
        towerLocation = TOWER_GRID[location]
        towerLocationCenter = (towerLocation[0] + (TOWER_GRID_SIZE / 2), towerLocation[1] + (TOWER_GRID_SIZE / 2))
        newTower = TOWER_TYPES[tower](towerLocationCenter)
        self.towers.append(newTower)

    def chooseAction(self):
        """ Chooses the next best tower and location to place """
        if random.random() < self.epsilon:
            #Pick randomly
            location = random.randint(0, STARTING_POSITIONS - 1)
            tower = random.randint(0, NUMBER_OF_TOWERS - 1)
            while not self.isLegal(location):
                location = random.randint(0, STARTING_POSITIONS)

            return location, tower
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

        randTower = random.choice(bestQValueIndices)
        return randTower[0], randTower[1]

    def findHighestQValue(self):
        ''' Returns the next highest value in the q-table '''
        return np.amax(self.qtable)

    def isLegal(self, placementIndex):
        ''' Returns true if the attempted position to place a tower is empty '''
        gridPosition = TOWER_GRID[placementIndex]
        gridPosition = (gridPosition[0] + (TOWER_GRID_SIZE / 2), gridPosition[1] + (TOWER_GRID_SIZE / 2))
        for i in range(len(self.towers)):
            if gridPosition == self.towers[i].position:
                return False
        return True

    def applyReward(self, score):
        ''' Updates the q-table for each placed tower with the overall reward / game score '''
        for location in range(len(self.towerPlacements)):
            if self.towerPlacements[location] != -1:
                self.updateQtable(self.towerPlacements[location], location, score)

    def updateQtable(self, tower, placement, score):
        ''' Updates the q-table after finishing one game '''
        self.qtable[placement][tower] = \
            self.qtable[placement][tower] + LEARN_RATE * \
            (score + DISCOUNT_RATE * self.findHighestQValue() - self.qtable[placement][tower])

    def saveData(self):
        ''' Saves the q-table to a file '''
        qtable = open("qtable.txt","w")

        qtableString = ''
        for row in self.qtable:
            for cell in row:
                qtableString += (','.join(str(cell) for n in row)) + '\n'

        qtable.write(qtableString)
        qtable.close()

    def loadData(self):
        ''' Loads previously qtable '''
        qtableFile = open("qtable.txt","r")
        qtableLines = qtableFile.readlines()

        qtable = []
        for line in qtableLines:
            line = line.strip('\n')
            line = line.split(',')

            row = []
            for n in line:
                row.append(float(n))
            qtable.append(row)

        return qtable


    def printQTable(self):
        print(self.qtable)
