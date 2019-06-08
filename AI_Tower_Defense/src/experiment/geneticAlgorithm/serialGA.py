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
            self.correctNumberOfTowers = generation + 1
            
            if self.collectWholeGameData:
                self.agent.initPopulation(self.correctNumberOfTowers)

            # play all of the games for each member of the population
            for i in range(POPULATION_SIZE):
                self.agent.setTowers(self.agent.population[i])
                # bool: visualMode, Towers: Agent.currentTowers, blank GameRecord, returns a record of the game stats, 
                # None for the deepQagent the game now expects 
                game = Game(self.visualMode, self.agent.currentTowers, GameRecord(), self.collectInnerGameData, None)
                # collects stats for the whole game
                record = game.run()
                # print(len(record.randomChoicesRecord))

                # print('\nList Size: ' + str(len(record.randomChoicesMade)))

                self.gameRecords.append(record)

            self.postGameProcessing()

        return
