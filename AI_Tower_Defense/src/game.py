import pygame
from pygame.locals import *
import os
import random

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

from ui.coin import Coin
from ui.menu import Menu

from constants.gameConstants import *


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
        self.enemies = [Trump(-10), Warrior(0), Zombie(30), Robot(0), Dino(15), Wizard(-25)]
        self.towers = [Obelisk(TOWER_POSITIONS[2]),  SquareTower(TOWER_POSITIONS[3]), Pyramid(TOWER_POSITIONS[5]), BirdCastle(TOWER_POSITIONS[7]), SquareTower(TOWER_POSITIONS[10]), Igloo(TOWER_POSITIONS[15]), WizardTower(TOWER_POSITIONS[8]), City((1180, 230))]
        self.numEnemiesPerLevel = 10
        self.remainingEnemies = 0
        self.score = 0
        self.lives = 10
        self.health = 100
        self.coinPosition = ((self.width - 150, 45))
        self.coins = Coin(self.coinPosition, 50)
        self.menu = Menu((400, 700), TOWER_TYPES)
        self.bg = pygame.image.load(os.path.join("../assets/map", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height)) #Scale to window (Make sure aspect ratio is the same)
        self.gameoverImage = pygame.image.load(os.path.join("../assets/other", "gameover.png"))
        self.gameoverImage = pygame.transform.scale(self.bg, (self.width, self.height))
        self.clicks = []
        self.spawnChance = 0.015

        #Fonts
        self.uiFont = pygame.font.SysFont('lucidagrandettc', 24)
        self.gameoverFont = pygame.font.SysFont('lucidagrandettc', 50)


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
                self.clicks.append(mousePosition)
                if SHOW_MOUSE_CLICKS:
                    print(self.clicks)

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
                self.remainingEnemies -= 1


    def spawnEnemies(self):
        '''
        Spawns enemies with random chance based on self.spawnChance
        This value should increase as levels get more difficult
        Caps number of enemies at once with self.numEnemiesPerLevel
        '''
        shouldSpawn = random.random()
        if shouldSpawn <= self.spawnChance and self.remainingEnemies < self.numEnemiesPerLevel:
            randVerticalOffset = random.randint(-Y_MAX_OFFSET, Y_MAX_OFFSET)
            randEnemyType = random.randint(0, len(ENEMY_TYPES) - 1)
            self.enemies.append(ENEMY_TYPES[randEnemyType](randVerticalOffset))


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
        self.coins.draw(self.win)

        #Render UI Text Elements
        self.displayTextUI(self.win, fps)

        self.menu.draw(self.win)

        #Update the window
        pygame.display.update()


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
        healthPosition = (WIN_WIDTH-180, WIN_HEIGHT-30)
        healthColor = (255, 255, 255)
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
