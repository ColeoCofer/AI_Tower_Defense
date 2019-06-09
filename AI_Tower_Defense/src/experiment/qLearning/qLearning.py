import pygame
import random
import pickle
import sys
import numpy as np

import matplotlib.pyplot as plt

from constants.aiConstants import *
from constants.gameConstants import *
from agent.qLearningAgent import QLearningAgent
from game.game import Game


class QLearning:

    def __init__(self, visualMode, trainingMode, loadQTableFromFile, saveQTableToFile, printGraphs):
        self.epsilon    = EPSILON

        # Array of position indices to track which locations have a tower placed there. -1 for empty position, and tower type index otherwise
        self.towerPlacements = [-1] * STARTING_POSITIONS
        self.qtable = np.zeros((STARTING_POSITIONS, NUMBER_OF_TOWERS))
        self.towers = []

        #Flags
        self.visualMode = visualMode
        self.trainingMode = trainingMode
        self.loadQTableFromFile = loadQTableFromFile
        self.saveQTableToFile = saveQTableToFile
        self.printGraphs = printGraphs


    def run(self):
        ''' Placeholder for children to define '''
        pass

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
                location = random.randint(0, STARTING_POSITIONS - 1)

            return location, tower
        else:
            #Greedily pick using Q-table
            bestQValueIndices = [(0, 0)]
            for location in range(STARTING_POSITIONS - 1):
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
        ''' Only updates Q Table when training mode is set'''
        if self.trainingMode:
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

        qtablePickleFile = open('qtable.pkl', 'wb')
        pickle.dump(self.qtable, qtablePickleFile)
        qtablePickleFile.close()

        #Append the game scores
        gameScoresFile = open("qLearningGameScores.txt", "w")
        gameScoresString = ','.join(str(n) for n in self.gameScores)
        gameScoresFile.write(gameScoresString)
        gameScoresFile.close()

    def loadData(self):
        ''' Loads previously qtable '''
        qtablePickleFile = open('qtable.pkl', 'rb')
        qtable = pickle.load(qtablePickleFile)
        print(f'\nLoaded qtable from file.\n')
        qtablePickleFile.close()

        # Load game scores
        qtableScoresFile = open("qLearningGameScores.txt", "r")
        scoresString = qtableScoresFile.readline()
        scores = [int(x) for x in scoresString.split(',')]
        print(f"Test Scores: {scores}")
        self.gameScores = scores

        return qtable

    def saveGraph(self):
        # plot the accuracy results from the training and test sets
        title = 'Game Scores'
        plt.plot(self.gameScores, label=title)
        plt.xlabel('Episode')
        plt.ylabel('Score')
        # plt.legend().set_visible(False)
        plt.savefig('qtableScores.png')

    def printQTable(self):
        print(self.qtable)
