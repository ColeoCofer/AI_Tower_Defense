import random as rand
import numpy as np
import matplotlib.pyplot as plt
import pygame

from constants.aiConstants import *
from constants.gameConstants import *
from agent.deepQagent import DeepQagent
from game.game import Game

DEEP_ITERATIONS = 100

# the game expects the following signature:
#      Game(visualMode, towers, gameRecord, collectInnerGameData, deepQagent)


class DeepQlearning:

    def __init__(self, visualMode):
        self.visualMode = visualMode


    def run(self):

        deepQ = DeepQagent()

        for iteration in range(DEEP_ITERATIONS):
            game = Game(self.visualMode, [], None, False, deepQ)
            deepQ = game.run()