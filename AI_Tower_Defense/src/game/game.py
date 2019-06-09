import pygame
from pygame.locals import *
import os
import random
import numpy as np
import copy

import enemies.zombie
from enemies.dino import Dino
from enemies.dragon import Dragon
from enemies.robot import Robot
from enemies.wizard import Wizard
from enemies.warrior import Warrior
from enemies.trump import Trump
from enemies.attackingEnemy import AttackingEnemy

from towers.squareTower import SquareTower
from towers.wizardTower import WizardTower
from towers.birdCastle import BirdCastle
from towers.obelisk import Obelisk
from towers.pyramid import Pyramid
from towers.city import City
from towers.igloo import Igloo

from ui.wallet import Wallet
from ui.menu import Menu

from agent.qLearningAgent import QLearningAgent

from constants.gameConstants import *
from constants.aiConstants import *
from constants.animationConstants import *

class InnerGameRecord:

    def __init__(self):
        self.currentScore = 0
        self.currentLevel = 0
        self.currentEnemiesKilled = 0
        self.currentNumberOfEnemies = 0
        self.currentNumberOfTowers = 0
        self.died = 0
        self.typeOfTowerPlaced = 0
        self.towerX = 0
        self.towerY = 0

        self.currentTowers = []


'''
Setup initial window and settings.
Renders all objects and background to the screen.
Handles user events (keyboard, mouse, etc)
Keeps track of score.
'''
class Game:

    def __init__(self, visualMode, towers, gameRecord, collectInnerGameData, deepQagent):

        self.visualMode           = visualMode
        self.gameRecord           = gameRecord
        self.collectInnerGameData = collectInnerGameData
        self.innerGameRecords     = []

        if self.visualMode:
            self.startBgMusic()

        ''' Initial window setup '''
        self.width  = WIN_WIDTH
        self.height = WIN_HEIGHT

        self.ticks = 0
        if self.visualMode == True:
            if FULLSCREEN_MODE:
                self.win = pygame.display.set_mode((self.width, self.height), FULLSCREEN | DOUBLEBUF)
            else:
                self.win = pygame.display.set_mode((self.width, self.height))
        else:
            self.win = None

        self.enemies      = []
        self.towerGrid    = [] #Holds all possible locations for a tower to be placed, and whether one is there or not, and the type of tower placed
        self.score        = 0
        self.health       = 200
        self.coinPosition = ((self.width - 150, 35))

        self.addedHealth  = 0
        self.addedSpeed   = 0
        self.towers       = towers
        self.towers.append(City((1180, 230)))

        # graphics
        self.menu          = Menu((350, 650), TOWER_TYPES)
        self.bg            = pygame.image.load(os.path.join("../assets/map", "bg.png"))
        self.bg            = pygame.transform.scale(self.bg, (self.width, self.height)) #Scale to window (Make sure aspect ratio is the same)
        self.gameoverImage = pygame.image.load(os.path.join("../assets/other", "gameover.png"))
        self.gameoverImage = pygame.transform.scale(self.bg, (self.width, self.height))
        self.clicks        = []

        #Level & Spawn
        self.level = 1
        self.enemiesSpawnedThisLevel = 0
        self.numEnemiesPerLevel      = 10
        self.remainingEnemies        = self.numEnemiesPerLevel
        self.totalEnemiesKilled      = 0
        self.spawnChance             = 0.005       # this can be throttled for testing
        self.enemySpawnProbs         = []
        self.showPathBounds          = False

        #Fonts
        self.uiFont       = pygame.font.SysFont('lucidagrandettc', 24)
        self.gameoverFont = pygame.font.SysFont('lucidagrandettc', 50)

        #Path
        self.pathBounds = []
        self.calcPathBounds()
        self.updateSpawnProbabilities()
        self.initTowerGrid()

        # deep Q things
        self.deepQagent        = deepQagent
        self.dqOldTowerGrid    = copy.deepcopy(self.towerGrid)
        self.dqLastTowerPlaced = None
        self.dqCurrentReward   = 0
        # deep Q reward things?? the damage dealt worries me for the igloo
        self.dqDamageDealt     = 0
        self.dqDamageTaken     = 0
        self.dqMaxedTowers     = False
        self.deepDecisions     = []

        self.isPaused          = False
        self.currSelectedTower = None   #Type of tower currently being selected from menu

        if self.deepQagent == None:
            self.wallet = Wallet(self.coinPosition, STARTING_COINS)
        else:
            self.wallet = Wallet(self.coinPosition, DEEP_STARTING_COINS)

        # print('Tower length = ' + str(len(self.towers)))
        # print('Starting Coins = ' + str(self.wallet.coins))


    def run(self):
        ''' Main game loop '''
        run = True
        playerHasQuit = False

        while run == True and playerHasQuit == False:

            playerHasQuit = self.handleEvents()
            if self.isPaused == False:
                # entry point for GAagent for data collection
                # if self.collectInnerGameData:
                #     if self.wallet.coins >= BUYING_THRESHOLD and len(self.towers) <= NUMBER_OF_STARTING_TOWERS:
                #         self.chooseNewTowerRandomly()
                self.spawnEnemies()
                self.towerHealthCheck()
                self.towersAttack()
                self.enemiesAttack()
                self.enemiesMove(self.ticks)
                self.removeEnemies()

                run = self.isAlive()
                self.ticks += 1

                # entry point for the deepQ agent to make decisions and learn from

                # all game states are the full tower grid of tuples
                # signature for update model:   update(oldGameState, newGameState, reward):
                #                                       oldGameState is the tower arrangment that is a result of the previous arrangment,
                #                                       newGameState is the current tower arrangement
                # signature for next action:    getNextAction(currentGameState):
                if self.deepQagent != None:
                    towerLength = len(self.towers)
                    if towerLength == NUMBER_OF_STARTING_TOWERS:
                        self.dqMaxedTowers = True
                    if self.wallet.coins >= DEEP_BUYING_THRESHOLD and towerLength < NUMBER_OF_STARTING_TOWERS and not self.dqMaxedTowers:

                        # this is returning a tower grid tuple from the agent
                        newTower = self.deepQagent.getNextAction(self.towerGrid)

                        # place the model chosen tower if possible
                        taken = False
                        for i in range(len(self.towerGrid)):
                            if self.towerGrid[i][0][0] == newTower[0][0] and self.towerGrid[i][0][1] == newTower[0][1]:
                                if self.towerGrid[i][2] != -1:
                                    # print('********Taken********')
                                    taken = True
                                    break
                                else:
                                    self.towerGrid[i] = ((self.towerGrid[i][0], True, newTower[2]))


                        # store a copy of the old tower grid state
                        oldTowerGrid = copy.deepcopy(self.towerGrid)

                        if not taken:
                            # should place a tower of the given type between 0-5, and with a position from the model
                            self.dqLastTowerPlaced = self.placeTower(newTower[2], newTower[0], -1)

                            # print('Tower length = ' + str(len(self.towers)))

                        else:
                            # this will be a flag to say that a tower was placed on an existing tower location when we
                            # calculate the results later
                            self.dqLastTowerPlaced = None

                        # store a copy of the new grid state
                        # newTowerGrid = copy.deepcopy(self.towerGrid)

                        # self.deepDecisions.append((oldTowerGrid, newTowerGrid, self.dqLastTowerPlaced))
                        self.deepDecisions.append((oldTowerGrid, self.dqLastTowerPlaced))


                self.draw()

        self.gameover()

        if self.collectInnerGameData or self.gameRecord != None:
            return self.gameRecord
        elif self.deepQagent != None:
            # return self.deepDecisions
            return self.deepQagent
        else:
            return


    # Randomly buys a new tower and places it for data collection
    def chooseNewTowerRandomly(self):

        while True:
            towerType = random.randint(0, NUMBER_OF_TOWERS - 1)
            towerPlacement = random.randint(0, STARTING_POSITIONS - 1)
            if self.towerGrid[towerPlacement][1] == False:
                # this will be used to map a tower to its record for data keeping purposes
                index = len(self.innerGameRecords)

                # place a random tower type in a random position
                self.towerGrid[towerPlacement] = ((TOWER_GRID[towerPlacement], True, towerType + 1))
                self.placeTower(towerType, TOWER_GRID[towerPlacement], index)

                # collect data for record
                newRecord = InnerGameRecord()
                newRecord.currentScore = self.score
                newRecord.currentLevel = self.level
                newRecord.currentEnemiesKilled = self.totalEnemiesKilled
                newRecord.currentNumberOfEnemies = len(self.enemies)
                newRecord.currentNumberOfTowers = len(self.towers)
                newRecord.typeOfTowerPlaced = towerType
                newRecord.towerX = TOWER_GRID[towerPlacement][0]
                newRecord.towerY = TOWER_GRID[towerPlacement][1]

                for i in range(STARTING_POSITIONS):
                    if self.towerGrid[i][1] == False:
                        newRecord.currentTowers.append(0)
                    else:
                        # included a digit in tower grids tuples to include tower type
                        newRecord.currentTowers.append(self.towerGrid[i][2])

                # add new record to the list
                self.innerGameRecords.append(newRecord)

                break

        return


    # goes through and removes dead towers from the list
    def towerHealthCheck(self):
        newTowers = []
        i = 0
        for i in range(len(self.towers)):
            # add alive towers back into the list
            if self.towers[i].health > 0:
                newTowers.append(self.towers[i])
            # a dead tower was found, free up its tile
            else:

                # if self.collectInnerGameData:
                    # this should update our record keeping to show that a tower that was placed has died
                    # self.innerGameRecords[self.towers[i].indexForRecordTable].died = 1
                j = 0
                for j in range(len(self.towerGrid)):
                    if self.towerGrid[j][0][0] == (self.towers[i].position[0] - (TOWER_GRID_SIZE / 2)) and self.towerGrid[j][0][1] == (self.towers[i].position[1] - (TOWER_GRID_SIZE / 2)):
                        self.towerGrid[j] = ((self.towerGrid[j][0], False, -1 ))

        self.towers = newTowers


    # cycles through all towers attack phase
    def towersAttack(self):
        for tower in self.towers:
            self.enemies = tower.attack(self.enemies, self.ticks)


    # cycles through any attacking enemies attack phase
    def enemiesAttack(self):
        for enemy in self.enemies:
            if isinstance(enemy, AttackingEnemy):
                self.towers = enemy.attack(self.towers, self.ticks)


    def enemiesMove(self, ticks):
        for enemy in self.enemies:
            enemy.move(ticks)


    ''' Handle keyboard and mouse events '''
    def handleEvents(self):
        '''
        Handle keyboard and mouse events
        Returns True if the user quits the game
        '''

        #Check for active pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            #Quit the game if the user hits the 'Q' key
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'q':
                    return True

            #Pause and unpause when p key is pushed
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'p':
                    if self.isPaused == True:
                        self.isPaused = False
                    else:
                        self.isPaused = True

            #Handle mouse hover over events for the menu
            self.menu.handleHoverEvents()

            #Store mouse clicks to determine path for enemies
            mousePosition = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                towerType, buttonWasSelected, towerLocation = self.menu.handleEvents(mousePosition, self.wallet, self.towerGrid)

                #Show path bounds if the user is placing a tower
                if buttonWasSelected == True:
                    self.currSelectedTower = towerType
                    self.showPathBounds = True

                #If not None, the user has purchased and placed a tower
                if towerType != None and towerLocation != None:
                    self.placeTower(towerType, towerLocation, -1)

                #Store & print mouse clicks for path finding and debugging
                if SHOW_CLICKS:
                    self.clicks.append(mousePosition)
                    print(self.clicks)
                return False

        return False


    ''' Removes enemies that have walked off screen'''
    def removeEnemies(self):

        for enemy in self.enemies:
            if enemy.x > WIN_WIDTH:
                if enemy.health <= enemy.initialHealth and enemy.health >= 0:
                    # Decrease by current health if it's less then the base starting health
                    self.health -= enemy.health
                else:
                    # Otherwise just decrease by the initial health
                    self.health -= enemy.initialHealth

            if enemy.health <= 0:
                self.score += enemy.initialHealth
                self.wallet.coins += enemy.coinReward

            if enemy.x > WIN_WIDTH or enemy.health <= 0:
                self.enemies.remove(enemy)
                self.remainingEnemies -= 1

                if enemy.health <= 0:
                    self.totalEnemiesKilled += 1


    def spawnEnemies(self):
        '''
        Spawns enemies with random chance based on self.spawnChance
        This value should increase as levels get more difficult
        Caps number of enemies at once with self.numEnemiesPerLevel
        '''
        shouldSpawn = random.random()

        #Check if there are still enemies to kill for this level
        if self.remainingEnemies > 0:
            #Should we spawn an enemy
            if shouldSpawn <= self.spawnChance:
                #Pick an enemy to spawn based on their probabilities
                randVerticalOffset = random.randint(-Y_MAX_OFFSET, (Y_MAX_OFFSET - int((Y_MAX_OFFSET / 2))))
                enemyToSpawn = np.random.choice(ENEMY_INDICES, 1, self.enemySpawnProbs)
                newEnemy = ENEMY_TYPES[enemyToSpawn[0]](randVerticalOffset)
                self.enemiesSpawnedThisLevel += 1
                self.updateEnemyHealth()
                self.updateEnemyWalkingSpeed()
                newEnemy.startingHealth +=  self.addedHealth
                newEnemy.health += self.addedHealth
                newEnemy.velocity += self.addedSpeed
                self.enemies.append(newEnemy)
        else:
            #New Level
            self.level += 1
            self.enemiesSpawnedThisLevel = 0
            #Increase chance to spawn an enemy by a percentage of the last spawn chance
            self.spawnChance += GLOBAL_SPAWN_PROB_INC * self.spawnChance
            self.numEnemiesPerLevel += ENEMY_PROB_INC * self.numEnemiesPerLevel
            self.remainingEnemies = self.numEnemiesPerLevel
            self.updateSpawnProbabilities()

            #Increase spawn chances for each enemy
            for enemy in self.enemies:
                newSpawnChance = enemy.spawnChance + ENEMY_SPAWN_INC
                #Check if we've maxed out spawn limit
                if newSpawnChance < enemy.spawnChanceLimit:
                    enemy.spawnChance = newSpawnChance
                else:
                    enemy.spawnChance = enemy.spawnChanceLimit


    def draw(self):
        '''
        Redraw objects onces per frame.
        Objects will be rendered sequentially,
        meaning the code at the end will be rendered above all.
        '''
        if self.visualMode:
            #Render the background
            self.win.blit(self.bg, (0, 0))

            #Displays click locations and rectangles where clicked
            self.showClicks()

            #Render coin animation
            self.wallet.draw(self.win)

            #Render UI Text Elements
            self.displayTextUI(self.win)

            self.menu.draw(self.win)

            if SHOW_PATH_BOUNDS and self.showPathBounds:
                self.drawPathBounds(self.win)
                self.drawTowerGrid(self.win)
                self.drawTowerRadius(self.win)


         # have towers fire even in non-visual mode
        for tower in self.towers:
            tower.draw(self.win, self.ticks, self.visualMode)

        #Render enemies
        for enemy in self.enemies:
            enemy.draw(self.win, self.ticks, self.visualMode)

        if self.visualMode:
            #Update the window
            pygame.display.update()



    def placeTower(self, towerType, towerLocation, index):
        if type(towerType) != int:
            towerType = TOWER_TYPES.index(towerType)

        newTowerLocation = (towerLocation[0] + (TOWER_GRID_SIZE / 2), towerLocation[1] + (TOWER_GRID_SIZE / 2))
        newTower = TOWER_TYPES[towerType](newTowerLocation)

        # this is just for the GA
        newTower.indexForRecordTable = index

        self.towers.append(newTower)
        self.showPathBounds = False
        self.wallet.spendCoins(newTower.cost)

        return newTower


    def calcPathBounds(self):
        '''
        Calculates an array of rectangles that describe the enemies path
        This function assumes that the ENEMY_PATH transitions are all straight lines
        Stores a list of rectanlges in self.pathBounds
        '''
        i = 0
        numPathPoints = len(ENEMY_PATH)
        for i in range(numPathPoints):
            if i < numPathPoints - 1:
                x1, y1 = ENEMY_PATH[i][0], ENEMY_PATH[i][1]
                x2, y2 = ENEMY_PATH[i+1][0], ENEMY_PATH[i+1][1]

                #Check what direction the points are moving and construct a rectangle
                if x1 == x2:
                    #Moving on y-axis
                    if y2 > y1: #Downward
                        rect = pygame.Rect((x1 - PATH_WIDTH_PX, y1 - PATH_WIDTH_PX), (PATH_WIDTH_PX*2, abs(y2 - y1)))
                    else:
                        rect = pygame.Rect((x2 - PATH_WIDTH_PX, y2 + PATH_WIDTH_PX), (PATH_WIDTH_PX*2, abs(y2 - y1)))

                else:
                    #Moving on x-axis
                    rect = pygame.Rect((x1 - PATH_WIDTH_PX, y1 - PATH_WIDTH_PX), (abs(x2 - x1), PATH_WIDTH_PX*2))

                self.pathBounds.append(rect)


    def drawPathBounds(self, win):
        ''' Draws rectangles around the path bounds '''
        for bound in self.pathBounds:
            self.bgRect = pygame.Surface((bound.width, bound.height))
            self.bgRect.set_alpha(125)
            self.bgRect.fill((200, 0, 0))
            win.blit(self.bgRect, (bound.x, bound.y))

    def drawTowerGrid(self, win):
        for tower in self.towerGrid:
            #Check if there's already a tower placed there
            if tower[1] == False:
                bgRect = pygame.Surface((GRID_DISPLAY_SIZE, GRID_DISPLAY_SIZE))
                bgRect.set_alpha(100)
                bgRect.fill((0, 100, 0))
                position = (tower[0][0] + (TOWER_GRID_SIZE - GRID_DISPLAY_SIZE) / 2, tower[0][1] + (TOWER_GRID_SIZE - GRID_DISPLAY_SIZE) / 2)
                self.win.blit(bgRect, position)

    def drawTowerRadius(self, win):
        ''' Draws circle around tower at attack radius '''

        if self.currSelectedTower != None:
            mousePosition = pygame.mouse.get_pos()
            tower = self.currSelectedTower((0,0))
            circleSurface = pygame.Surface((tower.attackRadius * 2, tower.attackRadius * 2))
            circleSurface.set_colorkey((0, 0, 0))
            circleSurface.set_alpha(75)
            pygame.draw.circle(circleSurface, (0, 50, 200), (tower.attackRadius, tower.attackRadius), tower.attackRadius, 0)
            self.win.blit(circleSurface, (mousePosition[0] - tower.attackRadius, mousePosition[1] - tower.attackRadius))


    def displayTextUI(self, win, ):
        ''' Render UI elements above all other graphics '''
        #Info about enemies
        numEnemiesText = "Enemies: " + str(self.enemiesSpawnedThisLevel) + " of " + str(int(self.numEnemiesPerLevel))
        numEnemiesPosition = (WIN_WIDTH-260, WIN_HEIGHT-50)
        self.displayText(numEnemiesText, numEnemiesPosition, self.uiFont, WHITE)

        self.displayText("Level: " + str(self.level), ((numEnemiesPosition[0] , numEnemiesPosition[1] - 25)), self.uiFont, WHITE)

        self.displayText("Dead: " + str(self.totalEnemiesKilled), ((numEnemiesPosition[0] , numEnemiesPosition[1] - 50)), self.uiFont, WHITE)
        self.displayText("Towers: " + str(len(self.towers)), (numEnemiesPosition[0], numEnemiesPosition[1] - 75), self.uiFont, WHITE)

        #Health
        healthText = "Health: " + str(int(self.health))
        healthPosition = (self.coinPosition[0] - 15, self.coinPosition[1] + 60)
        self.displayText(healthText, healthPosition, self.uiFont, self.getHealthColor())

        #Score
        self.displayText("Score: " + str(self.score), (self.coinPosition[0] - 20, self.coinPosition[1] + 30), self.uiFont, (250, 241, 95))

        #Paused
        if self.isPaused == True:
            self.displayText("PAUSED", ((WIN_WIDTH / 2) - 25, 60), self.uiFont, (200, 0, 0))


    def displayText(self, text, position, font, color):
        ''' Renders text at location using a specific font '''
        surface = font.render(text, False, color)
        self.win.blit(surface, position)


    def updateSpawnProbabilities(self):
        ''' Initialized list of enemy spawn probabilities '''
        for enemy in self.enemies:
            self.enemySpawnProbs.append(enemy.spawnChance)


    def updateEnemyWalkingSpeed(self):
        ''' Bumps up the enemy speed every 2 levels by 1 '''
        levelForIncrease = (self.level % NUMBER_LEVELS_SPEED_INCREASE) == 0
        if levelForIncrease:
            self.addedSpeed += SPEED_INCREASE


    def updateEnemyHealth(self):
        ''' Bumps up the enemy health every 3 levels by 2 '''
        levelForIncrease = (self.level % NUMBER_LEVELS_HEALTH_INCREASE) == 0
        if levelForIncrease:
            self.addedHealth += HEALTH_INCREASE


    def getHealthColor(self):
        ''' Changes the text color of the players health '''
        if self.health >= 90:
            return (23, 186, 39)
        elif self.health >= 75:
            return (184, 201, 34)
        elif self.health >= 60:
            return (201, 151, 34)
        elif self.health >= 45:
            return (201, 67, 34)
        else:
            return (178, 20, 12)


    def isAlive(self):
        return self.health > 0


    def initTowerGrid(self):
        '''
        Initializes tower grid based on hard coded values in TOWER_GRID
        Second value is True if a tower is placed in that location
        '''
        for location in TOWER_GRID:
            self.towerGrid.append((pygame.Rect(location, (TOWER_GRID_SIZE, TOWER_GRID_SIZE)), False, -1))


    def showClicks(self):
        ''' Displays click locations and rectangles to assist with towerGrid placement and logs coordinates to terminal '''
        if SHOW_CLICKS:
            #Display already placed squares
            for p in self.clicks:
                pygame.draw.circle(self.win, (255, 0, 0), (p[0], p[1]), 5, 0)
                bgRect = pygame.Surface((64, 64))
                bgRect.set_alpha(180)
                bgRect.fill((200, 0, 0))
                self.win.blit(bgRect, (p[0], p[1]))

            #Display square on mouse cursor
            mousePosition = pygame.mouse.get_pos()
            bgRect = pygame.Surface((64, 64))
            bgRect.set_alpha(180)
            bgRect.fill((0, 0, 200))
            self.win.blit(bgRect, (mousePosition[0], mousePosition[1]))


    # plays our awesome RenFair music
    def startBgMusic(self):
        if PLAY_BG_MUSIC and self.visualMode:
            randSong = random.randint(0, len(BG_MUSIC) - 1)
            pygame.mixer.music.load("../assets/music/background/" + BG_MUSIC[randSong])
            pygame.mixer.music.play(-1)


    def gameover(self):
        print('\nFinal Score:          ' + str(self.score))
        print('Total Enemies Killed: ' + str(self.totalEnemiesKilled))
        print('Final Level:          ' + str(self.level))
        print('Towers Intact:        ' + str(len(self.towers)-1))
        print('Coins:                ' + str(self.wallet.coins) + '\n')

        if self.gameRecord != None:
            self.gameRecord.fitnessScore = self.score
            self.gameRecord.level = self.level
            self.gameRecord.enemiesKilled = self.totalEnemiesKilled
            self.gameRecord.towersRemaining = len(self.towers) - 1
            self.gameRecord.earnings = self.wallet.coins

            # self.gameRecord.randomChoicesMade = self.innerGameRecords

        if self.deepQagent != None:
            self.updateDecisions()
            self.deepQagent.finalScore = self.score
            self.deepQagent.finalLevel = self.level


    def updateDecisions(self):
        # a decision: (oldTowerGrid, newTowerGrid, self.dqLastTowerPlaced) <-- reference to last tower placed
        for decision in self.deepDecisions:
            newReward = self.getReward(decision[1])
            # update the model
            # self.deepQagent.update(decision[0], decision[1], newReward)
            self.deepQagent.update(decision[0], self.towerGrid, newReward)


    def getReward(self, tower):
        reward = 0
        if tower != None:
            reward =  tower.damageDealtOnTurn * 5
            reward -= tower.damageTakenOnTurn * 2
            reward += self.score // 2            # reduce the influence of the final score
        else:
            reward += TOWER_POSITION_TAKEN_PENALTY

        return reward

TOWER_POSITION_TAKEN_PENALTY = -1000
