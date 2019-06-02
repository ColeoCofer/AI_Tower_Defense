from constants.gameConstants import *
import numpy as np

class QLearningAgent:

    def __init__(self):
        
        self.towers = []
        self.record = []
        self.currentScore = 0


    def initTowers(self):
        tempTowers = list(TOWER_GRID)
        np.random.shuffle(tempTowers)
        self.towers = tempTowers[:NUMBER_OF_STARTING_TOWERS]
        

    