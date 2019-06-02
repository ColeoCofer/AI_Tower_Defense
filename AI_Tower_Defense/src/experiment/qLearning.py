import pygame
import random
import sys

from constants.aiConstants import *
from constants.gameConstants import *
from agent.qLearningAgent import QLearningAgent
from game.game import Game

class QLearning:

    def __init__(self, agent):  
        self.agent = agent
        

    def run(self):
        game = Game(True, False, self.agent)
        game.run()

        return
        