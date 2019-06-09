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

DEEP_ITERATIONS = 1000
GENERATIONS_BETWEEN_UPDATE = 50
PARALLEL_MODE = False

# the game expects the following signature:
#      Game(visualMode, towers, gameRecord, collectInnerGameData, deepQagent)


class DeepQlearning:

    def __init__(self, visualMode):
        self.visualMode = visualMode
        self.agentQueue = []
        self.currentGameScore = 0


    def run(self):

        deepQ = DeepQagent()   
        saver = tf.train.Saver()
        # saver.restore(deepQ.session, "./deepQmodel/model.ckpt")
        highScore = 0
        highLevel = 0

        for iteration in range(DEEP_ITERATIONS):
            # if (iteration == DEEP_ITERATIONS - 1) and (not PARALLEL_MODE):   
            #     self.visualMode = True
            # if iteration % 10 == 0 and iteration != 0:
            #     self.visualMode = True
            # elif (iteration - 1) % 10 == 0 and iteration != 1:
            #     self.visualMode = True
            # else:
            #     self.visualMode = False
            # if iteration % 2 == 0:
            #     self.visualMode = True
            # else:
            #     self.visualMode = False
            # if iteration % 5 == 0 and iteration != 0:
            #     self.visualMode = True
            # else:
            #     self.visualMode = False
            self.visualMode = True

            print('\nIteration: ' + str(iteration + 1))

            game = Game(self.visualMode, [], None, False, deepQ)
            deepQ = game.run()

            if iteration % 100 == 0: 
                saver.save(deepQ.session, "./deepQmodel/model.ckpt")

        saver.save(deepQ.session, "./deepQmodel/model.ckpt")
