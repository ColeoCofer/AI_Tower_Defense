import pygame
from enum import Enum

from game.game import Game
from experiment.qLearning import QLearning
from experiment.geneticAlgorithm.parallelGA import ParallelGeneticAlgorithm
from experiment.geneticAlgorithm.serialGA import SerialGeneticAlgorithm
from experiment.deepQlearning import DeepQlearning

from agent.qLearningAgent import QLearningAgent
from agent.geneticAgent import GeneticAgent
from agent.deepQagent import DeepQagent

from constants.gameConstants import *


class MODE(Enum):
    manual           = 0,
    geneticAlgorithm = 1,
    qLearning        = 2,
    deepQlearning    = 3


GAME_MODE = MODE.deepQlearning  # Select which mode to run the game in
PARALLEL_MODE  = False          # Run a game on each processor core (only when visual_mode is off)
COLLECT_WHOLE_GAME_DATA = True  # Game data collection for the GA 
COLLECT_INNER_GAME_DATA = True  # "     "
VISUAL_MODE    = False          # Display Graphics
READ_FILE      = False          # Read model from file and continue training from it
SAVE_TO_DISK   = False          # Collect and store data
PRINT_GRAPHS   = False          # Prints graphs of score averages

# the game expects the following signature:
#      Game(visualMode, towers, gameRecord, collectInnerGameData, deepQagent)

def main():
    ''' Entry point for game '''

    #Setup Game
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("AI Tower Defense")

    # Determine game mode
    if GAME_MODE == MODE.manual:
        game = Game(True, [], None, False, None)
        game.run()
    elif GAME_MODE == MODE.geneticAlgorithm:
        if PARALLEL_MODE:
            gaAlgo = ParallelGeneticAlgorithm(VISUAL_MODE, READ_FILE, SAVE_TO_DISK, PRINT_GRAPHS, COLLECT_WHOLE_GAME_DATA, COLLECT_INNER_GAME_DATA)
        else:
            gaAlgo = SerialGeneticAlgorithm(VISUAL_MODE, READ_FILE, SAVE_TO_DISK, PRINT_GRAPHS, COLLECT_WHOLE_GAME_DATA, COLLECT_INNER_GAME_DATA)
        gaAlgo.run()
        
    elif GAME_MODE == MODE.qLearning:
        qLearning = QLearning(VISUAL_MODE)
        qLearning.run()

    elif GAME_MODE == MODE.deepQlearning:
        deepQ = DeepQlearning(VISUAL_MODE)
        deepQ.run()

    pygame.quit()


if __name__ == "__main__":
    main()
