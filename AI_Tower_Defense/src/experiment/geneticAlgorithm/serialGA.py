import random as rand
import numpy as np
import matplotlib.pyplot as plt
import pygame
from joblib import Parallel, delayed

from constants.aiConstants import *
from constants.gameConstants import *
from agent.geneticAgent import GeneticAgent
from game.game import Game
from .geneticAlgorithm import GeneticAlgorithm, GameRecord



class SerialGeneticAlgorithm(GeneticAlgorithm):

    def __init__(self, visualMode, readFile, saveToDisk, printGraphs):
        super().__init__(visualMode, readFile, saveToDisk, printGraphs)


    def run(self):
        
        if self.readFile:
            print("** Reading population from file **")
            self.agent.population = self.loadData()
        else:
            self.agent.initPopulation()

        # for i in range(POPULATION_SIZE):

#                 self.trainingMode = True
#                 self.visualMode = False

#                 self.agent.currentCitizenIndex = i
#                 self.agent.setTowers(self.agent.population[i])

#                 # bool: visualMode, bool: trainingMode, Agent: agent
#                 game = Game(self.visualMode, self.trainingMode, self.agent.currentTowers, None)
#                 game.run()

        for generation in range(MAX_GENERATIONS):
            # play all of the games for each member of the population
            for i in range(POPULATION_SIZE):
                self.agent.setTowers(self.agent.population[i])
                # bool: visualMode, Towers: Agent.currentTowers, blank GameRecord, returns a record of the game stats
                game = Game(self.visualMode, self.agent.currentTowers, GameRecord())
                self.gameRecords.append(game.run())

            self.postGameProcessing(generation)

        return


    # # performs the crossover of pairs of parent states to start to generate new children
    # def crossoverParents(self):
    #     newPopulation = list()
    #     populationSize = len(self.agent.population)

    #     i = 0
    #     while(i < populationSize):
    #         pivotPoint = self.getPivot()

    #         child1 = np.concatenate((self.agent.population[i][:pivotPoint], self.agent.population[i+1][pivotPoint:])).tolist()
    #         newPopulation.append(child1)

    #         if NUMBER_OF_CHILDREN == 2:
    #             child2 = np.concatenate((self.agent.population[i+1][:pivotPoint], self.agent.population[i][pivotPoint:])).tolist()
    #             newPopulation.append(child2)

    #         i += 2

    #     self.agent.population = newPopulation
