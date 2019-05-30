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

#Fullscreen will make the game run waaaay better
FULLSCREEN_MODE = True
PLAY_BG_MUSIC = False        #Set false to turn music off
SHOW_MOUSE_CLICKS = False   #If true will display dots where clicked, and print the coordinate in terminal
SHOW_PATH_BOUNDS = True     #If true will display bounds to enemy path

TOWER_POSITIONS = [(35, 294), (131, 289), (128, 181), (189, 151), (354, 150), (428, 387), (492, 383), (493, 261), (423, 264), (559, 211), (732, 207), (279, 302), (277, 380), (44, 427), (193, 430), (355, 519), (468, 517), (591, 516), (657, 351), (679, 412), (637, 416), (822, 341), (817, 285), (904, 182), (1152, 180), (1034, 180), (1160, 321), (1072, 320), (990, 321), (972, 422), (282, 458), (272, 149), (645, 209), (425, 200), (127, 233), (747, 458), (899, 455)]

TRAINING_MODE = False  #If true will uncap framerates
VISUAL_MODE = True     #Set false to stop rendering
FPS = 60

#Player
STARTING_COINS = 500

#Spawn Probabilities
GLOBAL_SPAWN_PROB_INC = 0.15   #Percent increase spawn chance per level
ENEMY_PROB_INC = 0.20          #Percent increase number of enemies per level
ENEMY_SPAWN_INC = 0.30         #Increments individual enemies spawn chances

#Window Dimensions
WIN_WIDTH = 1200
WIN_HEIGHT = 800

#Enemies
ENEMY_TYPES = [Zombie, Dino, Dragon, Robot, Wizard, Warrior, Trump]
ENEMY_INDICES = [0, 1, 2, 3, 4, 5, 6]
Y_MAX_OFFSET = 35  #yOffset along enemy walking path

#Towers
TOWER_TYPES = [SquareTower, BirdCastle, Igloo, WizardTower, Pyramid, Obelisk]

#Sounds
BG_MUSIC = ["old_town.mp3"]
