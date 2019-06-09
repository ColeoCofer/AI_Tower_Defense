from constants.aiConstants import *
from constants.gameConstants import * 
import random as rand
import tensorflow as tf
import numpy as np

INPUT_NODES = (NUMBER_OF_TOWERS + 1) * STARTING_POSITIONS    # the +1 is for the empty state  (798 input nodes currently)
OUTPUT_NODES = INPUT_NODES #(NUMBER_OF_TOWERS + 1) * STARTING_POSITIONS
NUMBER_OF_HIDDEN_NODES = OUTPUT_NODES


class DeepQagent:

    # making iterations smaller will decrease how long the agent explores and increase time spent
    def __init__(self, learningRate=0.1, discountRate=0.95, explorationRate=1.0, iterations=30000):
        
        self.learningRate = learningRate
        self.discountRate = discountRate
        self.explorationRate = 1.0                  # TODO consider how we are going to set these two to start
        self.explorationDelta = 1.0 / iterations    

        # Input has 798 input states elements (6 towers plus a blank times 114 grid tile locations)
        self.inputCount = INPUT_NODES
        # Output has 684 states as we should never choose placing nothing in a tower grid space
        self.outputCount = OUTPUT_NODES

        self.session = tf.Session()
        self.defineModel()
        self.session.run(self.initializer)

        # self.lastActions = []
        self.finalScore = 0
        self.finalLevel = 0

        self.deepDecisions = []


    # this gets ran once on creation of a new DeepQlearning object (init)
    # this defines how the input layer is constructed: self.modelInput
    # this defines how the output layer is structured: self.modelOutput
    def defineModel(self):
        self.modelInput = tf.placeholder(dtype=tf.float32, shape=[1, self.inputCount])

        # Two hidden layers of 50 neurons with sigmoid activation initialized to zero for stability
        fc1 = tf.layers.dense(self.modelInput, NUMBER_OF_HIDDEN_NODES, activation=tf.sigmoid, kernel_initializer=tf.constant_initializer(np.zeros((self.inputCount, NUMBER_OF_HIDDEN_NODES))))
        fc2 = tf.layers.dense(fc1, NUMBER_OF_HIDDEN_NODES, activation=tf.sigmoid, kernel_initializer=tf.constant_initializer(np.zeros((NUMBER_OF_HIDDEN_NODES, self.outputCount))))

        # output is a representation of the actions that could be taken, i.e. where to place a new tower
        self.modelOutput = tf.layers.dense(fc2, self.outputCount)
        self.targetOutput = tf.placeholder(shape=[1, self.outputCount], dtype=tf.float32)
        loss = tf.losses.mean_squared_error(self.targetOutput, self.modelOutput)
        
        # Optimizer adjusts weights to minimize loss
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learningRate).minimize(loss)
        
        # Initializer to set weights to initial values
        self.initializer = tf.global_variables_initializer()


    # the old and new states are the tower grid list from the game and need to be translated to the models form for states
    # we need to also pass in the reward for the previous action
    def update(self, oldGameState, newGameState, reward, action):
        
        # translate the tower grid arrangments into binary representations for the model to consume
        oldState = self.translateGameState(oldGameState)
        newState = self.translateGameState(newGameState)        
        
        # Train our model with new data, we have saved the previous action returned
        # to train the model with as actions
        self.train(oldState, action, reward, newState)

        # Reduce the exploration rate at each iteration
        if self.explorationRate > 0:
            self.explorationRate -= self.explorationDelta

    
    # this is just called by update to do the actual training
    def train(self, oldState, action, reward, newState):
        # Ask the model for the Q values of the old state
        oldStateQvalues = self.getQ(oldState)

        # Ask the model for the Q values of the new state
        newStateQvalues = self.getQ(newState)
        index = np.amax(action)
        # Real Q value for the action we took. This is what we will train towards.
        oldStateQvalues[index] = reward + self.discountRate * np.amax(newStateQvalues)
        
        # Setup training data 
        trainingInput = oldState
        targetOutput = [oldStateQvalues]
        trainingData = {self.modelInput: trainingInput, self.targetOutput: targetOutput}

        # Train
        self.session.run(self.optimizer, feed_dict=trainingData)


    # Model input: Single state of the tower gird represented by an array of tower positional values
    # Model output: Array of Q values for given input tower arrangement
    def getQ(self, state):
        return self.session.run(self.modelOutput, feed_dict={self.modelInput: state})[0]


    # this should be called from the game to supply the next action to take
    def getNextAction(self, gameState):
        if rand.random() > self.explorationRate: # Explore/Exploit
            # need to translate game state into model state
            currentState = self.translateGameState(gameState)
            newAction = self.greedyAction(currentState)
            # newAction = self.greedyAction(gameState)
            # saving this form of the action for the models next iteration
            # self.lastActions.append(newAction)
            return self.translateModelAction(newAction), newAction
            # return newAction

        else:
            randomAction = self.randomAction()
            # self.lastActions.append(randomAction)
            return self.translateModelAction(randomAction), randomAction
            # return randomAction


    # we should return an action in the format of the model, it will need translated into game form
    def greedyAction(self, currentState):
        action = np.zeros((OUTPUT_NODES,), dtype=int)
        newTower = np.argmax(self.getQ(currentState))
        action[newTower] = 1

        return action

    
    # this will return a random tower placement in model form, it will need translated to game form
    def randomAction(self):
        action = np.zeros((OUTPUT_NODES,), dtype=int)
        randindex = rand.randint(0, OUTPUT_NODES - 1)
        action[randindex] = 1

        return action


    # translate the tower grid of the game into a binary string of length 798 (7 tower states * 114 grid positions)
    def translateGameState(self, towerGrid):
        gameState = np.zeros((1, INPUT_NODES), dtype=int)
        step = NUMBER_OF_TOWERS + 1
        
        i = 0
        for location in towerGrid:
            # tower should be a 0-6 to represent no tower through all 6 tower types (the +1 is to shift the -1 that represents 
            # empty to be the proper location in our binary representation)
            tower = location[2] + 1
            gameState[0][i + tower] = 1
            i += step

        return gameState


    # translate the binary string of length 684 (6 tower states * 114 grid positions, it should only have a single 1 and the rest 0s) 
    # into a new tower position for the game
    def translateModelAction(self, newAction):        

        # get the index of the new tower being placed
        actionList = newAction.tolist()
        actionIndex = actionList.index(1)

        # this will give us an index between 0-113 which is for a grid position in the tower grid
        gridLocation = actionIndex // (NUMBER_OF_TOWERS + 1)
        # this will give us a number between 0-5 which is for a tower type which is a list from 0-5
        towerType = actionIndex %  (NUMBER_OF_TOWERS + 1)
        
        towerGridPosition = tuple((TOWER_GRID[gridLocation], True, towerType - 1))

        return towerGridPosition


class DataAgent:

    def __init__(self):

        self.towerPlacements = []
        self.lastActions = []
        self.currentTowerIndex = 0
        self.deepDecisions = []
        self.finalScore = 0
        self.finalLevel = 0

    def getNextTower(self):
        # newTower = self.towerPlacements.pop()
        return self.towerPlacements.pop()

    def addNextTower(self, tower):
        self.towerPlacements.append(tower)
        return