import pygame
import os
import random
from .enemy import Enemy

from projectile.projectile import DamageType

class Dragon(Enemy):

    spawnChance = 0.5
    spawnChanceLimit = 0.9
    startingHealth = 14                               # dragons have medium health
    coinReward = 30
    velocity = 20  #random.randint(8, 12)             # dragons are pretty fast

    def __init__(self, yOffset):
        super().__init__(yOffset)
        # self.startingHealth = 14                               # dragons have medium health
        # self.coinReward = 30
        self.health = self.startingHealth
        self.velocity = random.randint(8, 12)             # dragons are pretty fast
        self.weaknesses.append(DamageType.lazer)
        self.weaknesses.append(DamageType.poison)
        self.weaknesses.append(DamageType.lightning)      # dragons are not weak to fire
        self.superWeakness = DamageType.lightning         # dragons are super weak to lightning

        self.numImages = 4
        self.animationSpeed = 5
        self.healthBarYOffset = 30
        self.images = []

        # self.spawnChance = 0.5
        # self.spawnChanceLimit = 0.9


        #Load animation images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/dragon", "dragon_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
