import pygame

from game.game import Game
from experiment.qLearning import QLearning
from experiment.geneticAlgorithm import GeneticAlgorithm, GeneticAlgorithm2
from agent.qLearningAgent import QLearningAgent
from agent.geneticAgent import GeneticAgent


from constants.gameConstants import *

MANUAL_MODE = False
PARALLEL_MODE = True
GA_MODE = True
QLEARNING_MODE = False

def main():
    ''' Entry point for game '''

    # #Setup Game
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("AI Tower Defense")

    if GA_MODE:
        if MANUAL_MODE:
            game = Game(True, False, [], None)
            game.run()
        else:
            gaAgent = GeneticAgent()
            if PARALLEL_MODE:
                gaAlgo = GeneticAlgorithm(gaAgent)      # Parallel mode
            else:
                gaAlgo = GeneticAlgorithm2(gaAgent)     # Manual mode

            gaAlgo.run()

    pygame.quit()

    # qAgent = QLearningAgent()
    # qLearning = QLearning(qAgent)

    # qLearning.run()





if __name__ == "__main__":
    main()
