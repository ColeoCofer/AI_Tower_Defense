import random as rand
import numpy as np
import matplotlib.pyplot as plt
import pygame
import tensorflow as tf


from constants.aiConstants import *
from constants.gameConstants import *
from agent.deepQagent import DeepQagent
from game.game import Game

DEEP_ITERATIONS = 300

# the game expects the following signature:
#      Game(visualMode, towers, gameRecord, collectInnerGameData, deepQagent)


class DeepQlearning:

    def __init__(self, visualMode):
        self.visualMode = visualMode


    # a decision: (oldTowerGrid, newTowerGrid, self.dqLastTowerPlaced) <-- reference to last tower placed


    def run(self):

        deepQ = DeepQagent()
        saver = tf.train.Saver()

        saver.restore(deepQ.session, "./deepQmodel/model.ckpt")

        for iteration in range(DEEP_ITERATIONS):
            # if iteration % 20 == 0 and iteration != 0:
            if iteration == DEEP_ITERATIONS - 1:   
               self.visualMode = True
            else:
                self.visualMode = False

            game = Game(self.visualMode, [], None, False, deepQ)
            deepQ = game.run()

        saver.save(deepQ.session, "./deepQmodel/model.ckpt")
