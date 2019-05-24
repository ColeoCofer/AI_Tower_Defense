import pygame
import os
import random
from enemies.zombie import Zombie
from enemies.dino import Dino
from enemies.dragon import Dragon
from enemies.robot import Robot
from towers.squareTower import SquareTower
from ui.coin import Coin

TOWER_POSITIONS = [(28, 284), (72, 284), (126, 289), (121, 250), (124, 214), (126, 173), (128, 139), (172, 139), (224, 140), (269, 140), (311, 138), (360, 134), (433, 190), (431, 238), (430, 287), (428, 344), (427, 391), (467, 394), (505, 391), (504, 352), (463, 353), (463, 296), (503, 298), (503, 239), (506, 190), (554, 212), (601, 209), (647, 209), (692, 212), (727, 215), (770, 214), (816, 220), (803, 340), (841, 343), (800, 308), (839, 308), (798, 270), (844, 269), (845, 220), (867, 186), (923, 190), (968, 192), (1008, 188), (1039, 187), (1076, 186), (1110, 187), (1148, 187), (1175, 189), (14, 425), (57, 426), (99, 421), (138, 423), (178, 424), (223, 424), (270, 422), (261, 293), (297, 293), (296, 344), (258, 343), (259, 383), (291, 385), (290, 460), (293, 503), (361, 525), (408, 525), (455, 525), (494, 523), (556, 522), (595, 522), (642, 517), (638, 482), (636, 432), (631, 381), (632, 350), (680, 348), (678, 380), (676, 422), (735, 466), (689, 467), (781, 464), (931, 466), (982, 465), (979, 431), (975, 385), (975, 326), (1041, 328), (1081, 327), (1138, 326), (1175, 330)]
TRAINING_MODE = False  #If true will uncap framerates
VISUAL_MODE = True     #Set false to stop rendering
PLAY_BG_MUSIC = True      #Set false to turn music off
FPS = 60

#Window Dimensions
WIN_WIDTH = 1200
WIN_HEIGHT = 800

#Enemies
ENEMY_TYPES = [Zombie, Dino, Dragon]
Y_MAX_OFFSET = 20      #yOffset along enemy walking path

#Towers
TOWER_TYPES = [SquareTower]

#Sounds
BG_MUSIC = ["old_town.mp3", "get_it.mp3"]


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
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemies = [Dino(0), Zombie(0), Dino(0), Zombie(0), Dino(0), Zombie(0), Dino(0), Dragon(0), Dragon(0)]
        self.towers = [SquareTower(TOWER_POSITIONS[15]), SquareTower(TOWER_POSITIONS[1]), SquareTower(TOWER_POSITIONS[13]), SquareTower(TOWER_POSITIONS[8]), SquareTower(TOWER_POSITIONS[len(TOWER_POSITIONS) - 2]), SquareTower(TOWER_POSITIONS[len(TOWER_POSITIONS) - 5])]
        self.numEnemiesPerLevel = 1
        self.remainingEnemies = 0
        self.lives = 10
        self.coins = Coin((self.width - 140, 50), 50)
        self.bg = pygame.image.load(os.path.join("../assets/map", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height)) #Scale to window (Make sure aspect ratio is the same)
        self.clicks = [] #Temp
        self.spawnChance = 0.015

        #Fonts
        self.uiFont = pygame.font.SysFont('lucidagrandettc', 24)


    def run(self):
        ''' Main game loop '''
        clock = pygame.time.Clock()

        run = True
        while run:
            if TRAINING_MODE:
                clock.tick(FPS)

            self.spawnEnemies()
            self.handleEvents()
            self.towersAttack()
            self.removeEnemies()

            if VISUAL_MODE:
                self.draw(clock.get_fps())

        pygame.quit()


    def towersAttack(self):
        for tower in self.towers:
            self.enemies = tower.attack(self.enemies, self.win)

    def handleEvents(self):
        ''' Handle keyboard and mouse events '''

        #Check for active pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #Store mouse clicks to determine path for enemies
            mousePosition = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicks.append(mousePosition)
                print(self.clicks)


    def removeEnemies(self):
        ''' Removes enemies that have walked off screen'''
        enemiesToDelete = []
        for enemy in self.enemies:
            if enemy.x > WIN_WIDTH or enemy.health <= 0:
                self.enemies.remove(enemy)
                self.remainingEnemies -= 1

                if enemy.x > WIN_WIDTH:
                    self.lives -= 1


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
            # self.enemies.append(ENEMY_TYPES[randEnemyType](0))


    def draw(self, fps):
        '''
        Redraw objects onces per frame.
        Objects will be rendered sequentially,
        meaning the code at the end will be rendered above all.
        '''
        #Render the background
        self.win.blit(self.bg, (0, 0))

        #Uncomment to see clicked dots for path finding
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

        #Frames Per Second
        fpsText = "FPS: " + str(int(fps))
        fpsPosition = (15, 20)
        fpsColor = (255, 255, 255)
        fpsSurface = self.uiFont.render(fpsText, False, fpsColor)
        win.blit(fpsSurface, fpsPosition)


def startBgMusic():
    if PLAY_BG_MUSIC:
        randSong = random.randint(0, len(BG_MUSIC) - 1)
        pygame.mixer.music.load("../assets/music/background/" + BG_MUSIC[randSong])
        pygame.mixer.music.play(-1)


if __name__ == "__main__":
    main()
