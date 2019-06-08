import random as rand
import numpy as np
import matplotlib.pyplot as plt
import pygame
import tensorflow as tf
from joblib import Parallel, delayed


from constants.aiConstants import *
from constants.gameConstants import *
from agent.deepQagent import DeepQagent
from game.game import Game

DEEP_ITERATIONS = 1000
GENERATIONS_BETWEEN_UPDATE = 50
PARALLEL_MODE = True

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
        saver.restore(deepQ.session, "./deepQmodel/model.ckpt")
        
        for iteration in range(DEEP_ITERATIONS):
            if (iteration == DEEP_ITERATIONS - 1) and (not PARALLEL_MODE):   
                self.visualMode = True
            else:
                self.visualMode = False

            print('\nIteration: ' + str(iteration))

            game = Game(self.visualMode, [], None, False, deepQ)
            deepQ = game.run()

        saver.save(deepQ.session, "./deepQmodel/model.ckpt")
