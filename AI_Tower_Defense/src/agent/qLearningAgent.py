import numpy as np

from constants.gameConstants import *
from constants.aiConstants import *

class Qdata:

    def __init__(self):
        self.qTable = np.zeros((NUMBER_OF_TOWERS, STARTING_POSITIONS))
        #  self.towers = []
        self.gameScores = []
        #  self.currentScore = 0


class QLearningAgent:

    def __init__(self):
        self.record = Qdata()
        
    
    def initTowers(self):
        tempTowers = list(TOWER_GRID)
        np.random.shuffle(tempTowers)
        self.record.towers = tempTowers[:NUMBER_OF_STARTING_TOWERS]


    def updateRecord(self):
        return