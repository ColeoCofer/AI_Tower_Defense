from .qLearning import QLearning

from constants.aiConstants import *
from constants.gameConstants import *


class ParallelQLearning(QLearning):
    '''
    Parallel version of Q learning

    '''
    def __init__(self, visualMode, loadQTableFromFile, saveQTableToFile, printGraphs):
        super().__init__(visualMode, loadQTableFromFile, saveQTableToFile, printGraphs)

    def run(self):
        pass
