import random as rand
import numpy as np
import matplotlib.pyplot as plt
import pygame
import tensorflow as tf
from joblib import Parallel, delayed


from constants.aiConstants import *
from constants.gameConstants import *
from agent.deepQagent import DeepQagent, DataAgent
from game.game import Game

DEEP_ITERATIONS = 40
GENERATIONS_BETWEEN_UPDATE = 50
PARALLEL_MODE = False

# the game expects the following signature:
#      Game(visualMode, towers, gameRecord, collectInnerGameData, deepQagent)


class DeepQlearning:

    def __init__(self, visualMode):
        self.visualMode = visualMode
        self.agentQueue = []
        self.currentGameScore = 0
        self.scores = []
        self.levels = []
        self.dataAgents = []


    def run(self):

        masterDeepQ = DeepQagent()   
        saver = tf.train.Saver()
        # saver.restore(deepQ.session, "./deepQmodel/model.ckpt")

        for iteration in range(DEEP_ITERATIONS):
            self.dataAgents = []
            self.agentQueue = []
            self.scores = []
            self.levels = []
            for i in range(GENERATIONS_BETWEEN_UPDATE):
                agent = DataAgent()

                # get the 15 tower placements for the agent and remember the actions taken for later update
                for i in range(NUMBER_OF_STARTING_TOWERS):
                    gameAction, modelAction = masterDeepQ.getNextAction(agent.towerPlacements)
                    agent.addNextTower(gameAction)
                    agent.lastActions.append(modelAction)
            
                # spin up 100 agents at a time
                self.agentQueue.append(agent)

            self.dataAgents = Parallel(n_jobs=-1, verbose=0, backend="threading")(map(delayed(self.runGame), self.agentQueue))


            for dataAgent in self.dataAgents:
                # update the table with all of the decisions that were made
                for deepDecision, lastAction in zip(dataAgent.deepDecisions, dataAgent.lastActions):    
                    masterDeepQ.update(deepDecision[0], deepDecision[1], deepDecision[2], lastAction)
                self.scores.append(dataAgent.finalScore)
                self.levels.append(dataAgent.finalLevel)

            scoresForRound = sum(self.scores)
            levelsForRound = sum(self.levels)
            avgScore = scoresForRound / len(self.scores)
            avgLevel = levelsForRound / len(self.levels)

            print('**** DEEP Q-LEARNING END OF GENERATION ****')
            print('Average score for generation: ' + str(avgScore))
            print('Average level for round:      ' + str(avgLevel))

            # if iteration % 20 == 0:
            self.saveStats(avgScore, avgLevel)

            # if iteration % 100 == 0: 
            saver.save(masterDeepQ.session, "./deepQmodel/model.ckpt")

        saver.save(masterDeepQ.session, "./deepQmodel/model.ckpt")


    def runGame(self, agent):
        game = Game(self.visualMode, [], None, False, agent)
        return game.run()  



    def saveStats(self, avgScore, avgLevel):
        ''' Saves the last trained population so you can load it later and continue training '''
        statsFile = open("deep_stats.txt","a")
        levelToFile = ''
        scoreToFile = ''
        for score, level in zip(self.scores, self.levels):
            levelToFile += str(level) + ','
            scoreToFile += str(score) + ','
        toFile = levelToFile + str(avgLevel) + '\n' + scoreToFile + str(avgScore) + '\n'    

        statsFile.write(toFile)
        statsFile.close()