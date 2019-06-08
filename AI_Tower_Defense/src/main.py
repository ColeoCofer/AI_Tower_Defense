import pygame
from enum import Enum

from game.game import Game
from experiment.qLearning.serialQLearning import SerialQLearning
from experiment.qLearning.parallelQLearning import ParallelQLearning
from experiment.geneticAlgorithm.parallelGA import ParallelGeneticAlgorithm
from experiment.geneticAlgorithm.serialGA import SerialGeneticAlgorithm
from experiment.deepQlearning import DeepQlearning

from agent.geneticAgent import GeneticAgent
from constants.gameConstants import *


class MODE(Enum):
    manual           = 0,
    geneticAlgorithm = 1,
    qLearning        = 2,
    deepQlearning    = 3


GAME_MODE = MODE.geneticAlgorithm  # Select which mode to run the game in
PARALLEL_MODE  = True          # Run a game on each processor core (only when visual_mode is off)
COLLECT_WHOLE_GAME_DATA = False  # Game data collection for the GA 
COLLECT_INNER_GAME_DATA = True  # "     "
VISUAL_MODE    = False          # Display Graphics
READ_FILE      = False          # Read model from file and continue training from it
SAVE_TO_DISK   = True          # Collect and store data
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

    displaySettings()

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

        if PARALLEL_MODE:
            qLearning = ParallelQLearning(VISUAL_MODE, READ_FILE, SAVE_TO_DISK, PRINT_GRAPHS)
        else:
            qLearning = SerialQLearning(VISUAL_MODE, READ_FILE, SAVE_TO_DISK, PRINT_GRAPHS)
        qLearning.run()

    elif GAME_MODE == MODE.deepQlearning:
        deepQ = DeepQlearning(VISUAL_MODE)
        deepQ.run()

    pygame.quit()

def displaySettings():
    ''' Displays the current game settings '''
    print(f"\n=== AI Tower Defense Settings ===")
    print(f"Game Mode:              {GAME_MODE.name}")
    print(f"Parallel Mode:          {PARALLEL_MODE}")
    print(f"Visual Mode:            {VISUAL_MODE}")
    print(f"Load model from file:   {READ_FILE}")
    print(f"Save model to file:     {SAVE_TO_DISK}")
    print(f"Save graphs:            {PRINT_GRAPHS}\n")


if __name__ == "__main__":
    main()
