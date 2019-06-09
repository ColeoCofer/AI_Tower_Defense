import random as rand
import numpy as np
import matplotlib.pyplot as plt
import pygame
from joblib import Parallel, delayed


from constants.aiConstants import *
from constants.gameConstants import *
from agent.geneticAgent import GeneticAgent
from game.game import Game, InnerGameRecord


class GameRecord:

    def __init__(self):
        self.earnings = 0
        
        self.numberOfTowers = 0
        self.fitnessScore = 0
        self.level = 0
        self.enemiesKilled = 0
        self.towersRemaining = 0
        self.population = []

        self.randomChoicesMade = []
        


class GeneticAlgorithm:

    def __init__(self, visualMode, readFile, saveToDisk, printGraphs, collectWholeGameData, collectInnerGameData):
        
        self.agent                 = GeneticAgent()
        self.visualMode            = False
        self.gameRecords           = []
        self.towersForGeneration   = []
        self.averageScores         = []
        self.averageScoreMax       = 0
        self.highScore             = 0
        self.highestLevel          = 0
        self.correctNumberOfTowers = 0
        self.visualMode            = visualMode
        self.readFile              = readFile
        self.saveToDisk            = saveToDisk
        self.printGraphs           = printGraphs
        self.collectWholeGameData  = collectWholeGameData
        self.collectInnerGameData  = collectInnerGameData



    # base class stub
    def run(self):
        pass


    # saves the current populations to a text file
    def saveData(self):
        populationString = ''
        gameRecord = ''

        if self.collectWholeGameData:
            dataCollectionFile = open("ga_data.txt","a")
            for record in self.gameRecords:
                gameRecord += str(record.numberOfTowers) + ',' + str(record.fitnessScore) + ',' + str(record.level) + ',' + str(record.enemiesKilled) + ',' + str(record.towersRemaining) + ',' + (','.join(str(int(n)) for n in record.population)) + '\n'
        
            dataCollectionFile.write(gameRecord)
            dataCollectionFile.close()
        else:
            ''' Saves the last trained population so you can load it later and continue training '''
            lastFitFile = open("lastfit_gen.txt","w")
            for citizen in self.agent.population:
                populationString += (','.join(str(int(n)) for n in citizen)) + '\n'

            lastFitFile.write(populationString)
            lastFitFile.close()

        if self.collectInnerGameData:
            dataCollectionFile = open("deep_data.txt","a")
            gameRecord = ''
            # peel off a game record for a generation at a time
            for record in self.gameRecords:
                # peel off the individual tower placement decision that were made
                for n in record.randomChoicesMade:
                    gameRecord += str(record.towersRemaining) + ',' + str(record.fitnessScore) + ',' + str(record.level) + ',' + str(record.enemiesKilled) + ',' +  \
                                  str(n.currentScore) + ',' + str(n.currentLevel) + ',' + str(n.currentEnemiesKilled) + ',' + str(n.currentNumberOfEnemies) + ',' + str(n.currentNumberOfTowers) + ',' +  \
                                  str(n.died) + ',' + str(n.typeOfTowerPlaced) + ',' + str(n.towerX) + ',' + str(n.towerY) + ',' + (','.join(str(int(m)) for m in n.currentTowers)) + '\n'
            dataCollectionFile.write(gameRecord)
            dataCollectionFile.close()

        # Index  Length:128
        # ----------------------------------------------------
        # 0:  Number of remaining towers when game ended
        # 1:  Final score of the game
        # 2:  Final level reached in the game
        # 3:  Total enemies killed in the game
        # 4:  Current score when the tower placement was made
        # 5:  Current level when the tower placement was made
        # 6:  Current number of enemies killed when the tower placement was made
        # 7:  Current number of alove enemies when the tower placement was made
        # 8:  Current number of placed towers when the new tower placement was made
        # 9:  Did the tower that is placed die before the end of the game (0: No, 1: Yes)
        # 10: The type of the tower placed (0-5)
        # 11: The x-position on the screen of the tower that has been placed
        # 12: The y-position on the screen of the tower that has been placed
        # 13-126: The digital representation of the tower grid and its constituents  

        averageScoresFile = open("averageScores.txt", "w")
        averageScoreString = ','.join(str(n) for n in self.averageScores)
        averageScoresFile.write(averageScoreString)
        averageScoresFile.close()


    # calls all of the common functions to update fitness scores, populations, and stats
    def postGameProcessing(self):
        newFitnessScores = []
        for data in self.gameRecords:
            newFitnessScores.append(data.fitnessScore)
            if data.fitnessScore > self.highScore:
                self.highScore = data.fitnessScore
            if data.level > self.highestLevel:
                self.highestLevel = data.level

        self.agent.fitnessScores = newFitnessScores

        # normalize fitness scores  
        averageScore = self.normalizeFitnessOfPopulation()
        if averageScore > self.averageScoreMax:
            self.averageScoreMax = averageScore
        self.averageScores.append(averageScore)

        print('\nAverage score for generation ' + str(self.correctNumberOfTowers) + ': ' + str(averageScore))
        print('Largest Average so far:          ' + str(self.averageScoreMax))
        print('High Score so far:               ' + str(self.highScore))
        print('Highest Level Reached:           ' + str(self.highestLevel))

        # create the new population for crossover based off of the probabilities from the fitness scores
        self.selectPopulationForCrossover()
        # perform the crossing over of pairs in the population
        self.crossoverParents()
        # perform the random mutation on the children
        self.mutateChildren()
        self.agent.fitnessScores = []

        if self.saveToDisk:
            self.saveData()

        if self.printGraphs and self.correctNumberOfTowers % int((0.2 * MAX_GENERATIONS)):
            self.printGraph()

        self.currentTowers = []

        return


    # load populations from a text file
    def loadData(self):
        ''' Loads previously saved trained population for GA so you can continue training '''
        populationFile = open("lastfit_gen.txt","r")
        fileLines = populationFile.readlines()
        populationList = []
        for line in fileLines:
            line = line.strip('\n')
            line = line.split(',')

            citizen = np.zeros((len(TOWER_GRID),), dtype=int)
            i = 0
            for n in line:
                citizen[i] = int(n)
                i += 1
            populationList.append(citizen)

        return populationList


    # print the average fitness graph
    def printGraph(self):
        # plot the accuracy results from the training and test sets
        title = 'Average Fitness'
        plt.plot(self.averageScores, label=title)
        plt.xlabel('Generations')
        plt.ylabel('Average Fitness')
        plt.legend(loc='best')
        plt.show()

        return


    # return a random pivot index
    def getPivot(self):
        return rand.randint(0, STARTING_POSITIONS-1)


    # return True if a citizen has exactly 20 towers
    def hasCorrectNumberOfTowers(self, citizen):
        towerCount = 0
        for tower in citizen:
            if tower != 0:
                towerCount += 1
        # print('Tower Count: ' + str(towerCount))
        # print('Self number: ' + str(self.correctNumberOfTowers))
        if towerCount == NUMBER_OF_STARTING_TOWERS:
            return True

        return False


    # normalizes fitness scores for the entire population
    def normalizeFitnessOfPopulation(self):
        populationSize = len(self.agent.population)

        sumOfFitnessScores = sum(self.agent.fitnessScores)
        for i in range(len(self.agent.fitnessScores)):
            self.agent.fitnessScores[i] /= sumOfFitnessScores
        averageFitnessScore = sumOfFitnessScores / populationSize

        return averageFitnessScore


    # performs the crossover of pairs of parent states to start to generate new children
    def crossoverParents(self):
        newPopulation = list()
        populationSize = len(self.agent.population)

        i = 0
        while(i < populationSize):
            while True:
                pivotPoint = self.getPivot()

                child1 = np.concatenate((self.agent.population[i][:pivotPoint], self.agent.population[i+1][pivotPoint:])).tolist()
                if NUMBER_OF_CHILDREN == 2:
                    child2 = np.concatenate((self.agent.population[i+1][:pivotPoint], self.agent.population[i][pivotPoint:])).tolist()

                if self.hasCorrectNumberOfTowers(child1) and self.hasCorrectNumberOfTowers(child2):
                    break

            newPopulation.append(child1)

            if NUMBER_OF_CHILDREN == 2:
                newPopulation.append(child2)

            i += 2

        self.agent.population = newPopulation


    # perform the random mutation on the location of the n-queens
    def mutateChildren(self):
        newPopulation = list()
        for citizen in self.agent.population:
            mutate = rand.random()
            if mutate <= MUTATION_PCT:
                repeat = True
                while(repeat):
                    locationToMutate = rand.randint(0, STARTING_POSITIONS - 1)
                    # new tower location to mutate should not be empty
                    if citizen[locationToMutate] == 0:
                        continue
                    else:
                        while(True):
                            newLocation = rand.randint(0, STARTING_POSITIONS - 1)
                            # ensure that we are not placing it in the new location and that the new location is not occupied
                            if (newLocation != locationToMutate) and (citizen[newLocation] == 0):
                                # randomly select a new tower type  TODO  Do we want to keep the same tower type??
                                citizen[newLocation] = rand.randint(1, NUMBER_OF_TOWERS)
                                citizen[locationToMutate] = 0
                                repeat = False
                                break

            newPopulation.append(citizen)

        self.agent.population = newPopulation


    # randomly generates a new population to subject to crossover based on their fitness score ratio to the whole
    def selectPopulationForCrossover(self):
        newPopulation = list()
        populationSize = len(self.agent.population)

        # this will take the best 20% of the population for survival of the fittest
        n = populationSize // FITTEST_POPULATION_FRACTION

        if NUMBER_OF_CHILDREN == 1:
            populationMultiplier = 2
        else:
            populationMultiplier = 1

        # translate fitness scores to ranges between 0.0-1.0 to select from randomly
        if SURVIVAL_OF_THE_FITTEST:
            fitParents = np.argpartition(self.agent.fitnessScores, -n)[-n:]
            i = 0
            while i < (populationSize * populationMultiplier):
                for fitParent in fitParents:
                    newPopulation.append(self.agent.population[fitParent])
                i += n

        else:
            print(self.agent.fitnessScores)
            # partition the fitness scores into buckets, thats why it is skipping the first index
            for i in range(1, populationSize):
                self.agent.fitnessScores[i] += self.agent.fitnessScores[i-1]


            # randomly pick new members for the population based on their fitness probabilities
            for i in range(populationSize * populationMultiplier):
                index = 0
                current = rand.random()
                for j in range(populationSize):
                    if current <= self.agent.fitnessScores[j]:
                        index = j
                        break
                newPopulation.append(self.agent.population[index])

        self.agent.population = newPopulation
