import pygame

from game.game import Game
from experiment.qLearning import QLearning
from experiment.geneticAlgorithm.parallelGA import ParallelGeneticAlgorithm
from experiment.geneticAlgorithm.serialGA import SerialGeneticAlgorithm

from agent.qLearningAgent import QLearningAgent
from agent.geneticAgent import GeneticAgent

from constants.gameConstants import *


GA_MODE        = True
QLEARNING_MODE = False

MANUAL_MODE    = False
PARALLEL_MODE  = False

VISUAL_MODE    = False

READ_FILE      = False
SAVE_TO_DISK   = False
PRINT_GRAPHS   = False


def main():
    ''' Entry point for game '''

    # #Setup Game
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("AI Tower Defense")

    if GA_MODE:
        if MANUAL_MODE:
            game = Game(True, [], None)
            game.run()
        else:
            if PARALLEL_MODE:
                gaAlgo = ParallelGeneticAlgorithm(VISUAL_MODE, READ_FILE, SAVE_TO_DISK, PRINT_GRAPHS)   # Parallel mode
            else:
                gaAlgo = SerialGeneticAlgorithm(VISUAL_MODE, READ_FILE, SAVE_TO_DISK, PRINT_GRAPHS)     # Manual mode

            gaAlgo.run()

    pygame.quit()

 

if __name__ == "__main__":
    main()