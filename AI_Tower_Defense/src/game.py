import pygame
from pygame.locals import *
import os
import random
import numpy as np

from enemies.zombie import Zombie
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

from constants.gameConstants import *
from constants.animationConstants import *


def main():
    ''' Entry point for game '''
    #Setup Game
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    startBgMusic()
    pygame.display.set_caption("AI Tower Defense")

    #Kick off main game loop
    g = Game()
    g.run()

'''
Setup initial window and settings.
Renders all objects and background to the screen.
Handles user events (keyboard, mouse, etc)
Keeps track of score.
'''
class Game:
    def __init__(self):
        ''' Initial window setup '''
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT

        if FULLSCREEN_MODE:
            self.win = pygame.display.set_mode((self.width, self.height), FULLSCREEN | DOUBLEBUF)
        else:
            self.win = pygame.display.set_mode((self.width, self.height))

        self.win.set_alpha(None)
        self.enemies = [Zombie(0), Zombie(10)]
        self.towers = [City((1180, 230))]
        self.score = 0
        self.lives = 10
        self.health = 100
        self.coinPosition = ((self.width - 150, 35))
        self.wallet = Wallet(self.coinPosition, STARTING_COINS)
        self.menu = Menu((350, 650), TOWER_TYPES)
        self.bg = pygame.image.load(os.path.join("../assets/map", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height)) #Scale to window (Make sure aspect ratio is the same)
        self.gameoverImage = pygame.image.load(os.path.join("../assets/other", "gameover.png"))
        self.gameoverImage = pygame.transform.scale(self.bg, (self.width, self.height))
        self.clicks = []

        #Level & Spawn
        self.numEnemiesPerLevel = 10
        self.remainingEnemies = self.numEnemiesPerLevel
        self.totalEnemiesKilled = 0
        self.spawnChance = 0.0055
        self.enemySpawnProbs = []
        self.showPathBounds = False

        #Fonts
        self.uiFont = pygame.font.SysFont('lucidagrandettc', 24)
        self.gameoverFont = pygame.font.SysFont('lucidagrandettc', 50)

        #Path
        self.pathBounds = []
        self.calcPathBounds()
        self.initSpawnProbabilities()


    def run(self):
        ''' Main game loop '''
        clock = pygame.time.Clock()
        run = True
        playerHasQuit = False

        while run == True and playerHasQuit == False:
            if TRAINING_MODE:
                clock.tick(FPS)

            self.spawnEnemies()
            playerHasQuit = self.handleEvents()
            self.towerHealthCheck()
            self.towersAttack()
            self.enemiesAttack()
            self.removeEnemies()
            run = self.isAlive()

            if VISUAL_MODE:
                self.draw(clock.get_fps())

        self.gameover()
        pygame.quit()


    # goes through and removes dead towers from the list
    def towerHealthCheck(self):
        newTowers = []
        for tower in self.towers:
            if tower.health > 0:
                newTowers.append(tower)

        self.towers = newTowers


    # cycles through all towers attack phase
    def towersAttack(self):
        for tower in self.towers:
            self.enemies = tower.attack(self.enemies, self.win)


    # cycles through any attacking enemies attack phase
    def enemiesAttack(self):
        for enemy in self.enemies:
            if isinstance(enemy, AttackingEnemy):
                self.towers = enemy.attack(self.towers, self.win)


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

            #Store mouse clicks to determine path for enemies
            mousePosition = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                towerType, buttonWasSelected = self.menu.handleEvents(mousePosition, self.wallet, self.pathBounds)

                #Show path bounds if the user is placing a tower
                if buttonWasSelected == True:
                    self.showPathBounds = True

                #If not None, the user has purchased and placed a tower
                if towerType != None:
                    self.placeTower(towerType)

                #Store & print mouse clicks for path finding and debugging
                if SHOW_MOUSE_CLICKS:
                    self.clicks.append(mousePosition)
                    print(self.clicks)
                return False

        return False


    ''' Removes enemies that have walked off screen'''
    def removeEnemies(self):
        enemiesToDelete = []
        for enemy in self.enemies:
            if enemy.x > WIN_WIDTH:
                self.lives -= 1
                self.health -= enemy.health

            if enemy.health <= 0:
                self.score += enemy.maxHealth

            if enemy.x > WIN_WIDTH or enemy.health <= 0:
                self.enemies.remove(enemy)
                self.totalEnemiesKilled += 1
                self.remainingEnemies -= 1


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
                randVerticalOffset = random.randint(-Y_MAX_OFFSET, Y_MAX_OFFSET)
                enemyToSpawn = np.random.choice(ENEMY_INDICES, 1, self.enemySpawnProbs)
                self.enemies.append(ENEMY_TYPES[enemyToSpawn[0]](randVerticalOffset))
                #randEnemyType = random.randint(0, len(ENEMY_TYPES) - 1)
                #self.enemies.append(ENEMY_TYPES[randEnemyType](randVerticalOffset))
        else:
            #New Level
            #Increase chance to spawn an enemy by a percentage of the last spawn chance
            self.spawnChance += GLOBAL_SPAWN_PROB_INC * self.spawnChance
            self.numEnemiesPerLevel += ENEMY_PROB_INC * self.numEnemiesPerLevel
            self.remainingEnemies = self.numEnemiesPerLevel

            #Increase spawn chances for each enemy
            for enemy in self.enemies:
                newSpawnChance = enemy.spawnChance + ENEMY_SPAWN_INC

                #Check if we've maxed out spawn limit
                if newSpawnChance < enemy.spawnChanceLimit:
                    enemy.spawnChance = newSpawnChance
                else:
                    enemy.spawnChance = enemy.spawnChanceLimit

        # if shouldSpawn <= self.spawnChance and self.remainingEnemies > 0:  #self.remainingEnemies > self.numEnemiesPerLevel:

            #On level change:
            #Increase game spawnChance
            #Increase individual enemies spawnChance
            #Increase numEnemiesPerLevel
            #Increase enemy speed? health?


    def draw(self, fps):
        '''
        Redraw objects onces per frame.
        Objects will be rendered sequentially,
        meaning the code at the end will be rendered above all.
        '''

        #Render the background
        self.win.blit(self.bg, (0, 0))

        #Uncomment to see clicked dots for path findings
        if SHOW_MOUSE_CLICKS:
            for p in self.clicks:
                pygame.draw.circle(self.win, (255, 0, 0), (p[0], p[1]), 5, 0)

        #Render towers
        for tower in self.towers:
            tower.draw(self.win)

        #Render enemies
        for enemy in self.enemies:
            enemy.draw(self.win)

        #Render coin animation
        self.wallet.draw(self.win)

        #Render UI Text Elements
        self.displayTextUI(self.win, fps)

        self.menu.draw(self.win)

        if SHOW_PATH_BOUNDS and self.showPathBounds:
            self.drawPathBounds(self.win)

        #Update the window
        pygame.display.update()

    def placeTower(self, towerType):
        mousePosition = pygame.mouse.get_pos()
        i = 0
        for i in range(len(TOWER_TYPES)):
            if TOWER_TYPES[i] == towerType:
                self.towers.append(TOWER_TYPES[i](mousePosition))
                self.showPathBounds = False


    def calcPathBounds(self):
        '''
        Calculates an array of rectangles that describe the enemies path
        This function assumes that the ENEMY_PATH transitions are all straight lines
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



    def displayTextUI(self, win, fps):
        ''' Render UI elements above all other graphics '''

        #Enemies Remaining Surface UI
        numEnemiesText = "Enemies: " + str(len(self.enemies))
        numEnemiesPosition = (WIN_WIDTH-180, WIN_HEIGHT-50)
        numEnemiesColor = (255, 255, 255)
        numEnemiesSurface = self.uiFont.render(numEnemiesText, False, numEnemiesColor)
        win.blit(numEnemiesSurface, numEnemiesPosition)

        #Health Remaining Surface UI
        healthText = "Health: " + str(self.health)
        healthPosition = (self.coinPosition[0] - 15, self.coinPosition[1] + 60)
        healthColor = self.getHealthColor()
        healthSurface = self.uiFont.render(healthText, False, healthColor)
        win.blit(healthSurface, healthPosition)

        #Frames Per Second
        fpsText = "FPS: " + str(int(fps))
        fpsPosition = (15, 20)
        fpsColor = (255, 255, 255)
        fpsSurface = self.uiFont.render(fpsText, False, fpsColor)
        win.blit(fpsSurface, fpsPosition)

        #Score
        scoreText = "Score: " + str(self.score)
        scorePosition = (self.coinPosition[0], self.coinPosition[1] + 30)
        scoreColor = (250, 241, 95)
        scoreSurface = self.uiFont.render(scoreText, False, scoreColor)
        win.blit(scoreSurface, scorePosition)

    def initSpawnProbabilities(self):
        ''' Initialized list of enemy spawn probabilities '''
        for enemy in self.enemies:
            self.enemySpawnProbs.append(enemy.spawnChance)

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

    def gameover(self):
        ''' I can't for the life of me get this to be displayed'''
        self.win.blit(self.gameoverImage, (0, 0))
        pygame.display.update()


# plays our awesome RenFair music
def startBgMusic():
    if PLAY_BG_MUSIC:
        randSong = random.randint(0, len(BG_MUSIC) - 1)
        pygame.mixer.music.load("../assets/music/background/" + BG_MUSIC[randSong])
        pygame.mixer.music.play(-1)


if __name__ == "__main__":
    main()
