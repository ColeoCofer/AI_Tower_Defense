import pygame
from game.game import Game
from experiment.qLearning import QLearning
from agent.qLearningAgent import QLearningAgent

def main():
    ''' Entry point for game '''
    #Setup Game
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_caption("AI Tower Defense")

    qAgent = QLearningAgent()
    qLearning = QLearning(qAgent)

    qLearning.run()



if __name__ == "__main__":
    main()