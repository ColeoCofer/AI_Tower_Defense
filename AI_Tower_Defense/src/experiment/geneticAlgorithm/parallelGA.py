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



class ParallelGeneticAlgorithm(GeneticAlgorithm):

    def __init__(self, visualMode, readFile, saveToDisk, printGraphs):
        super().__init__(visualMode, readFile, saveToDisk, printGraphs)
        

    def run(self):
        
        if self.readFile:
            print("** Reading population from file **")
            self.agent.population = self.loadData()
        else:
            self.agent.initPopulation()

        for generation in range(MAX_GENERATIONS):
            self.gameRecords = []
            self.towersForGeneration = []

            # create a list of all of the populations tower arrangements, and a blank list of records to feed to the parallel call
            for i in range(POPULATION_SIZE):
                self.towersForGeneration.append(self.agent.setTowers(self.agent.population[i]))
                self.gameRecords.append(GameRecord())

            # play all of the games for each member of the population
            # n_jobs=-1 means to ask for all of the processor cores
            self.gameRecords = Parallel(n_jobs=-1, verbose=0, backend="threading")(map(delayed(self.runGame), self.towersForGeneration, self.gameRecords))

            # process the results of the generation
            self.postGameProcessing(generation)

        return


    def runGame(self, towers, gameRecord):
        # bool: visualMode, list: towers, record for individual game data
        game = Game(self.visualMode, towers, gameRecord)
        return game.run()
