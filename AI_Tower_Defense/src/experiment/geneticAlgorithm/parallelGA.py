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


    def __init__(self, visualMode, readFile, saveToDisk, printGraphs, collectWholeGameData, collectInnerGameData):
        super().__init__(visualMode, readFile, saveToDisk, printGraphs, collectWholeGameData, collectInnerGameData)

    def run(self):

        if self.readFile:
            print("** Reading population from file **")
            self.agent.population = self.loadData()
        elif not self.collectWholeGameData:
            self.agent.initPopulation(NUMBER_OF_STARTING_TOWERS)

        for generation in range(MAX_GENERATIONS):
            self.gameRecords = []
            self.towersForGeneration = []
            # self.correctNumberOfTowers = generation + 1

            # initializes the population to one with the same number of towers as the generation for data collection
            if self.collectWholeGameData:
                self.agent.initPopulation(self.correctNumberOfTowers)

            # create a list of all of the populations tower arrangements, and a blank list of records to feed to the parallel call
            for i in range(POPULATION_SIZE):
                gameRecord = GameRecord()

                # this is capturing whole game stats, we will also collect in-game stats
                if self.collectWholeGameData:
                    # record population for data collection for other algorithms
                    gameRecord.population = self.agent.population[i]
                    # record the generation number as that as how many towers they get for data collection
                    gameRecord.numberOfTowers = generation

                self.towersForGeneration.append(self.agent.setTowers(self.agent.population[i]))
                self.gameRecords.append(gameRecord)

            # play all of the games for each member of the population
            # n_jobs=-1 means to ask for all of the processor cores
            self.gameRecords = Parallel(n_jobs=-1, verbose=0, backend="threading")(map(delayed(self.runGame), self.towersForGeneration, self.gameRecords))

            # process the results of the generation
            self.postGameProcessing()

        return


    def runGame(self, towers, gameRecord):
        # bool: visualMode, list: towers, record for individual game data, None for the deepQ agent the game now expects
        game = Game(self.visualMode, towers, gameRecord, self.collectInnerGameData, None)
        return game.run()
