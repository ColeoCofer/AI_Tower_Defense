from constants.gameConstants import *
import numpy as np

class Qdata:

    def __init__(self):
        self.qTable = np.zeros((STARTING_POSITIONS, NUMBER_OF_TOWERS))
        self.towers = []
        self.gameScores = []
        self.currentScore = 0


class QLearningAgent:

    def __init__(self):
        self.record = Qdata()
        
    
    def initTowers(self):
        tempTowers = list(TOWER_GRID)
        np.random.shuffle(tempTowers)
        self.record.towers = tempTowers[:NUMBER_OF_STARTING_TOWERS]


    def updateRecord(self):

        return