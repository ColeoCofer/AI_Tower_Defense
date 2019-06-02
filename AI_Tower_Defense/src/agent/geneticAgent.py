import numpy as np
import random as rand

from constants.gameConstants import *
from constants.aiConstants import *


class GeneticAgent:

    def __init__(self):
        self.towers = []
        self.population = []
        self.fitnessScores = []

        self.gameScores = []
        self.currentScore = 0
        
    
    # Creates an initial randomized population
    def initPopulation(self):
        population = list()

        for i in range(POPULATION_SIZE):
            # creates random strings for the populations to start
            population = np.zeros(STARTING_POSITIONS, int)

            for j in range(NUMBER_OF_STARTING_TOWERS):
                population[j] = rand.randint(1, NUMBER_OF_TOWERS)
            np.random.shuffle(population)
            self.population.append(population)


