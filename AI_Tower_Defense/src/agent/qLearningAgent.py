from constants.gameConstants import *
import numpy as np

class Qrecord:

    def __init__(self):
        self.qTable = []
        self.towers = []
        self.currentScore = 0


class QLearningAgent:

    def __init__(self):
        self.record = Qrecord()
        
    

    def initTowers(self):
        tempTowers = list(TOWER_GRID)
        np.random.shuffle(tempTowers)
        self.record.towers = tempTowers[:NUMBER_OF_STARTING_TOWERS]

    
    def train(self):

        return    

    