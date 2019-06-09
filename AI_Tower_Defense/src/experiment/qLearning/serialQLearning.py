from game.game import Game
from .qLearning import QLearning

import matplotlib.pyplot as plt

from constants.aiConstants import *
from constants.gameConstants import *

NUM_GAMES_BEFORE_SAVING_GRAPH = 20
NUM_GAMES_BEFORE_PLOTTING_SCORE = 10

class SerialQLearning(QLearning):
    def __init__(self, visualMode, trainingMode, loadQTableFromFile, saveQTableToFile, printGraphs):
        super().__init__(visualMode, trainingMode, loadQTableFromFile, saveQTableToFile, printGraphs)
        self.gameScores = []


    def run(self):
        ''' Kicks off multiple game instances and updates the q-table after each game ends '''
        # Read in saved qtable and continue training
        if self.loadQTableFromFile:
            self.qtable = self.loadData()

        # Number of games to train on
        for N in range(N_EPISODES):
            print(f"Game #: {N + 1}")
            # decrease epsilon every 50 episodes
            if self.epsilon >= 0 and self.trainingMode == True:
                if N % EPSILON_PERIOD == 0:
                    self.epsilon -= EPSILON_STEP

            self.towers = []
            # Each step determines the next tower to place
            for M in range(NUMBER_OF_STARTING_TOWERS):
                location, tower = self.chooseAction()
                self.addTower(location, tower)

            # Run the game until it's over
            game = Game(self.visualMode, self.towers, None, None, None)
            game.run()

            # Update q-table for each tower placement using the final game score
            self.applyReward(game.score)

            # We don't want too many plotted points
            if N % NUM_GAMES_BEFORE_PLOTTING_SCORE == 0:
                self.gameScores.append(game.score)

            # Save the model to load later
            self.saveData()

            # Save a graph every x games
            if self.printGraphs and (N + 1) % NUM_GAMES_BEFORE_SAVING_GRAPH == 0:
                self.saveGraph()
