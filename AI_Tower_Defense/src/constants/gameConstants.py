from enemies.zombie import Zombie
from enemies.dino import Dino
from enemies.dragon import Dragon
from enemies.robot import Robot
from enemies.wizard import Wizard
from enemies.warrior import Warrior
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
PLAY_BG_MUSIC = False      #Set false to turn music off

TOWER_POSITIONS = [(35, 294), (131, 289), (128, 181), (189, 151), (354, 150), (428, 387), (492, 383), (493, 261), (423, 264), (559, 211), (732, 207), (279, 302), (277, 380), (44, 427), (193, 430), (355, 519), (468, 517), (591, 516), (657, 351), (679, 412), (637, 416), (822, 341), (817, 285), (904, 182), (1152, 180), (1034, 180), (1160, 321), (1072, 320), (990, 321), (972, 422), (282, 458), (272, 149), (645, 209), (425, 200), (127, 233), (747, 458), (899, 455)]

TRAINING_MODE = False  #If true will uncap framerates
VISUAL_MODE = True     #Set false to stop rendering
FPS = 60

#Window Dimensions
WIN_WIDTH = 1200
WIN_HEIGHT = 800

#Enemies
ENEMY_TYPES = [Zombie, Dino, Dragon, Robot, Wizard, Warrior]
Y_MAX_OFFSET = 35  #yOffset along enemy walking path

#Towers
TOWER_TYPES = [SquareTower]

#Sounds
BG_MUSIC = ["old_town.mp3"]
