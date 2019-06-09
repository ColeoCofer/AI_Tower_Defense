from .qLearning import QLearning

from constants.aiConstants import *
from constants.gameConstants import *


class ParallelQLearning(QLearning):
    '''
    Parallel version of Q learning

    '''
    def __init__(self, visualMode, trainingMode, loadQTableFromFile, saveQTableToFile, printGraphs):
        super().__init__(visualMode, trainingMode, loadQTableFromFile, saveQTableToFile, printGraphs)

    def run(self):
        pass
