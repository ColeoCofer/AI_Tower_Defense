import pygame

from game.game import Game
from experiment.qLearning import QLearning
from experiment.geneticAlgorithm import GeneticAlgorithm
from agent.qLearningAgent import QLearningAgent
from agent.geneticAgent import GeneticAgent


from constants.gameConstants import *

def main():
    ''' Entry point for game '''
    #Setup Game
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("AI Tower Defense")

    # bool: visualMode, bool: trainingMode, Agent: agent
    # game = Game(True, False, None)
    # game.run()

    gaAgent = GeneticAgent()
    gaAlgo = GeneticAlgorithm(gaAgent)
    gaAlgo.run()

    # qAgent = QLearningAgent()
    # qLearning = QLearning(qAgent)

    # qLearning.run()





if __name__ == "__main__":
    main()