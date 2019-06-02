import pygame
import random
import sys

from constants.aiConstants import *
from constants.gameConstants import *
from agent.qLearningAgent import QLearningAgent
from game.game import Game


class QLearning:

    def __init__(self, agent):  
        self.agent        = agent
        self.epsilon      = EPSILON

        self.trainingMode = False
        self.visualMode   = False

    def run(self):
        self.agent.initTowers()
       
        for N in range(N_EPISODES):
            # decrease epsilon every 50 episodes
            if self.epsilon >= 0 and self.trainingMode == ON:
                if N % EPSILON_PERIOD == 0:
                    self.epsilon -= EPSILON_STEP

            for M in range(M_STEPS):
                # Robby makes a move using epsilon-greedy
                robby, reward = nextAction(epsilon, Qmatrix, robby, board, actionTax)
                # Update the Q-matrix after each action
                if trainingModeOn:
                    Qmatrix = updateQmatrix(eta, gamma, Qmatrix, robby, reward, robbiesOldState, robbiesOldPosition)


                # bool: visualMode, bool: trainingMode, Agent: agent
                game = Game(self.visualMode, self.trainingMode, self.agent)
                game.run()

        return
        