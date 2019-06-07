from enums import *
from constants.aiConstants import *
from constants.gameConstants import * 
import random as rand
import tensorflow as tf
import numpy as np

NUMBER_OF_HIDDEN_NODES = 30
INPUT_NODES = (NUMBER_OF_TOWERS + 1) * STARTING_POSITIONS
OUTPUT_NODES = INPUT_NODES


class deepQagent:

    def __init__(self, learningRate=0.1, discountRate=0.95, explorationRate=1.0, iterations=10000):
        self.learningRate = learningRate
        self.discountRate = discountRate
        self.explorationRate = 1.0                
        self.explorationStep = 1.0 / iterations  

        # Input has 798 input states elements (6 towers plus a blank times 114 grid tile locations)
        self.inputCount = INPUT_NODES
        # Output is the same length as the input layer and indicates where a tower should be placed
        self.outputCount = OUTPUT_NODES

        self.session = tf.Session()
        self.defineModel()
        self.session.run(self.initializer)


    def defineModel(self):
        self.modelInput = tf.placeholder(dtype=tf.float32, shape=[None, self.inputCount])

        # Two hidden layers of 50 neurons with sigmoid activation initialized to zero for stability
        fc1 = tf.layers.dense(self.modelInput, NUMBER_OF_HIDDEN_NODES, activation=tf.sigmoid, kernel_initializer=tf.constant_initializer(np.zeros((self.inputCount, NUMBER_OF_HIDDEN_NODES))))
        fc2 = tf.layers.dense(fc1, NUMBER_OF_HIDDEN_NODES, activation=tf.sigmoid, kernel_initializer=tf.constant_initializer(np.zeros((NUMBER_OF_HIDDEN_NODES, self.outputCount))))

        # output is a representation of the actions that could be taken
        self.modelOutput = tf.layers.dense(fc2, self.outputCount)

        self.targetOutput = tf.placeholder(shape=[None, self.outputCount], dtype=tf.float32)
        loss = tf.losses.mean_squared_error(self.targetOutput, self.modelOutput)
        # Optimizer adjusts weights to minimize loss
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learningRate).minimize(loss)
        # Initializer to set weights to initial values
        self.initializer = tf.global_variables_initializer()


    def update(self, oldState, newState, action, reward):
        # Train our model with new data
        self.train(oldState, action, reward, newState)

        # Reduce the exploration rate at each iteration
        if self.explorationRate > 0:
            self.explorationRate -= self.explorationStep

    def train(self, oldState, action, reward, newState):
        # Ask the model for the Q values of the old state
        oldStateQvalues = self.getQ(oldState)

        # Ask the model for the Q values of the new state
        newStateQvalues = self.getQ(newState)

        # Real Q value for the action we took. This is what we will train towards.
        oldStateQvalues[action] = reward + self.discountRate * np.amax(newStateQvalues)
        
        # Setup training data 
        trainingInput = self.toInputVector(oldState)
        targetOutput = [oldStateQvalues]
        trainingData = {self.modelInput: trainingInput, self.targetOutput: targetOutput}

        # Train
        self.session.run(self.optimizer, feed_dict=trainingData)


    def getQ(self, state):
        # Model input: Single state represented by array of input values
        # Model output: Array of Q values for single state
        return self.session.run(self.modelOutput, feed_dict={self.modelInput: self.toInputVector(state)})[0]


    def getNextAction(self, state):
        if rand.random() > self.explorationRate: # Explore/Exploit
            return self.greedyAction(state)
        else:
            return self.randomAction()


    def greedyAction(self, state):
        action = np.zeros((OUTPUT_NODES,), dtype=int)
        newTower = np.argmax(self.getQ(state))
        action[newTower] = 1

        return action

    
    def randomAction(self):
        action = np.zeros((OUTPUT_NODES,), dtype=int)
        randindex = rand.randint(0, OUTPUT_NODES - 1)
        action[randindex] = 1

        return action