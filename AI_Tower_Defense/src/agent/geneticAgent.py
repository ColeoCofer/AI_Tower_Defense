import numpy as np
import random as rand

from constants.gameConstants import *
from constants.aiConstants import *


class GeneticAgent:

    def __init__(self):
        self.currentTowers       = []
        self.population          = []
        self.fitnessScores       = []

        self.gameScores          = []
        self.earnings            = []
        self.enemiesKilled       = []
        self.towersRemaining     = []

        self.currentScore        = 0
        self.currentCitizenIndex = 0



    # Creates an initial randomized population
    def initPopulation(self, numberOfStartingTowers):
        self.population = []
        for i in range(POPULATION_SIZE):
            # creates random strings for the populations to start
            citizen = np.zeros((STARTING_POSITIONS,), dtype=int)
            # randomly pick a tower type (1-6 right now)
            for j in range(numberOfStartingTowers):
                citizen[j] = rand.randint(1, NUMBER_OF_TOWERS)
            np.random.shuffle(citizen)
            self.population.append(citizen)


    def setTowers(self, citizen):
        self.currentTowers = []

        # iterate through the list representation of the towers
        for i in range(len(citizen)):
            # if the current tile position is not blank in the string representation
            #   place the corresonding tower in that position
            if citizen[i] != 0:
                currentTower = int(citizen[i]) - 1
                newTowerPosition = ((TOWER_GRID[i][0] + (TOWER_GRID_SIZE / 2), TOWER_GRID[i][1] + (TOWER_GRID_SIZE / 2)))
                newTower = TOWER_TYPES[currentTower](newTowerPosition)
                self.currentTowers.append(newTower)

        return self.currentTowers
