import random as rand
import numpy as np
import matplotlib.pyplot as plt
import pygame

from constants.aiConstants import *
from constants.gameConstants import *
from agent.deepQagent import DeepQagent
from game.game import Game

DEEP_ITERATIONS = 1000

# the game expects the following signature:
#      Game(visualMode, towers, gameRecord, collectInnerGameData, deepQagent)


class DeepQlearning:

    def __init__(self, visualMode):
        self.visualMode = visualMode


    def run(self):

        deepQ = DeepQagent()

        for iteration in range(DEEP_ITERATIONS):
            # if iteration % 20 == 0 and iteration != 0:
            if iteration == DEEP_ITERATIONS - 1:   
               self.visualMode = True
            else:
                self.visualMode = False

            game = Game(self.visualMode, [], None, False, deepQ)
            deepQ = game.run()