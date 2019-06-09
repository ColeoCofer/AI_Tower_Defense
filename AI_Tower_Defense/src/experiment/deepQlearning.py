import random as rand
import numpy as np
import matplotlib.pyplot as plt
import pygame
import tensorflow as tf
# from joblib import Parallel, delayed


from constants.aiConstants import *
from constants.gameConstants import *
from agent.deepQagent import DeepQagent
from game.game import Game

DEEP_ITERATIONS = 2000
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


    def run(self):

        deepQ = DeepQagent()   
        saver = tf.train.Saver()
        # saver.restore(deepQ.session, "./deepQmodel/model.ckpt")

        for iteration in range(DEEP_ITERATIONS):
            if iteration % 5 == 0 and iteration != 0:
                self.visualMode = True
            else: 
                self.visualMode = False
        
            print('\nIteration: ' + str(iteration + 1))
            game = Game(self.visualMode, [], None, False, deepQ)
            deepQ = game.run()

            self.scores.append(deepQ.finalScore)
            self.levels.append(deepQ.finalLevel)

            if iteration % 20 == 0:
                self.saveStats()

            if iteration % 100 == 0: 
                saver.save(deepQ.session, "./deepQmodel/model.ckpt")

        saver.save(deepQ.session, "./deepQmodel/model.ckpt")


    def saveStats(self):
        ''' Saves the last trained population so you can load it later and continue training '''
        statsFile = open("deep_stats.txt","w")
        levelToFile = ''
        scoreToFile = ''
        for score, level in zip(self.scores, self.levels):
            levelToFile += str(level) + ','
            scoreToFile += str(score) + ','
        toFile = levelToFile + '\n' + scoreToFile     

        statsFile.write(toFile)
        statsFile.close()