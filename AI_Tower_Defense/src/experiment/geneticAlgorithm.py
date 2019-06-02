import random as rand
import numpy as np

from constants.aiConstants import *
from constants.gameConstants import *
from agent.geneticAgent import GeneticAgent
from game.game import Game


class GeneticAlgorithm:

    def __init__(self, agent):  
        self.agent = agent
        self.currentFitnessScores = []

        self.trainingMode = False
        self.visualMode   = True


    def run(self):

        return


    # return a random pivot index
    def getPivot(self):
        return rand.randint(0, STARTING_POSITIONS-1) 

    
    # generates fitness scores for the entire population
    def normalizeFitnessOfPopulation(self):
        populationSize = len(self.agent.population)
        
        sumOfFitnessScores = np.sum(self.currentFitnessScores)
        self.currentFitnessScores /= sumOfFitnessScores
        averageFitnessScore = sumOfFitnessScores / populationSize

        return averageFitnessScore


    # performs the crossover of pairs of parent states to start to generate new children
    def crossoverParents(self):
        newPopulation = list()
        populationSize = len(self.agent.population)
        i = 0
        while(i < populationSize):
            pivotPoint = self.getPivot()
        
            child1 = np.concatenate((self.agent.population[i][:pivotPoint], self.agent.population[i+1][pivotPoint:]))
            newPopulation.append(child1)

            if NUMBER_OF_CHILDREN == 2:
                child2 = np.concatenate((self.agent.population[i+1][:pivotPoint], self.agent.population[i][pivotPoint:]))  
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
    n = populationSize // 5
    
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