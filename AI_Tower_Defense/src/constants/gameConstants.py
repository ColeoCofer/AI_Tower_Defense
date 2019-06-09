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

FULLSCREEN_MODE = False     #Display in fullscreen (runs better for high res screens)
PLAY_BG_MUSIC = False        #Set false to turn music off

SHOW_CLICKS = False         #If true will display dots where clicked, and print the coordinate in terminal
SHOW_PATH_BOUNDS = True     #If true will display bounds to enemy path

# Locations where towers may be placed
TOWER_GRID = [(92, 252), (17, 254), (93, 406), (17, 407), (169, 406), (246, 264), (247, 334), (245, 406), (245, 474), (169, 475), (92, 475), (18, 476), (91, 178), (16, 178), (159, 106), (227, 106), (296, 107), (365, 107), (90, 106), (16, 106), (405, 346), (465, 346), (792, 299), (790, 232), (538, 174), (605, 174), (672, 174), (739, 166), (805, 164), (622, 327), (622, 395), (621, 463), (546, 501), (482, 501), (417, 500), (352, 501), (703, 438), (770, 437), (838, 436), (905, 436), (873, 139), (940, 139), (1010, 139), (1080, 140), (951, 293), (1019, 293), (1088, 295), (952, 362), (1019, 361), (1087, 361), (434, 108), (502, 109), (569, 108), (637, 108), (704, 105), (774, 101), (975, 435), (1044, 434), (1112, 432), (702, 504), (770, 503), (838, 502), (905, 502), (975, 501), (1045, 500), (1112, 500), (620, 531), (14, 39), (88, 38), (157, 39), (227, 38), (295, 39), (363, 41), (431, 39), (499, 42), (564, 42), (634, 41), (703, 37), (772, 34), (871, 72), (939, 72), (937, 6), (869, 6), (244, 542), (169, 543), (92, 542), (17, 542), (352, 567), (418, 566), (482, 566), (545, 566), (703, 570), (770, 570), (833, 568), (905, 568), (976, 567), (1044, 567), (1111, 565), (16, 609), (92, 611), (168, 611), (244, 610), (907, 637), (976, 636), (1043, 635), (1109, 634), (243, 678), (166, 680), (90, 679), (16, 678), (401, 279), (461, 279), (401, 204), (465, 204)]

# Number of possible grid locations
STARTING_POSITIONS = len(TOWER_GRID)

# Grid square size
TOWER_GRID_SIZE = 64

# Smaller dark spot when manually placing the towers
GRID_DISPLAY_SIZE = 45

TRAINING_MODE = True    #If true will uncap framerates  TODO  not sure this is used anymore
VISUAL_MODE = False     #Set false to stop rendering
FPS = 60

#Player
STARTING_COINS   = 500
BUYING_THRESHOLD = 200         # the number of coins to trigger the AI to decide where to buy a new tower

#Spawn Probabilities
GLOBAL_SPAWN_PROB_INC = 0.25   # Percent increase spawn chance per level
ENEMY_PROB_INC = 0.20          # Percent increase number of enemies per level
ENEMY_SPAWN_INC = 0.30         # Increments individual enemies spawn chances

#Level increase constants
# STARTING_LEVEL  = 10
HEALTH_INCREASE = 2                     # how much health is added to enemies when increased
SPEED_INCREASE  = 1                     # how much speed is added to enemies when increased
NUMBER_LEVELS_HEALTH_INCREASE = 3       # how many levels before an enemy health increase
NUMBER_LEVELS_SPEED_INCREASE  = 4       # how many levels before an enemy speed increase

#Window Dimensions
WIN_WIDTH = 1200
WIN_HEIGHT = 800

#Enemies
ENEMY_TYPES   = [Zombie, Dino, Dragon, Robot, Wizard, Warrior, Trump]
ENEMY_INDICES = [0, 1, 2, 3, 4, 5, 6]
Y_MAX_OFFSET  = 35  #yOffset along enemy walking path, causes the enemies to not be walking on same exact line

#Towers
TOWER_TYPES      = [SquareTower, BirdCastle, Igloo, WizardTower, Pyramid, Obelisk]
TOWER_INDICES    = [0, 1, 2, 3, 4, 5]
NUMBER_OF_TOWERS = len(TOWER_TYPES)

#Sounds
BG_MUSIC = ["old_town.mp3"]
