import os
import pygame
import random
import math
from .rangeProjectile import RangeProjectile
from .projectile import DamageType

class Cannonball(RangeProjectile):
    def __init__(self, towerPosition, enemy):
        super().__init__(towerPosition, enemy)
        self.damage = 1
        self.damageType = DamageType.exploding
        self.reloadTime = 3000
        self.velocity = 100
        self.numImages = 1
        self.width = 30
        self.height = 30
        self.attackAnimationDuration = 15000

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/cannonball", "cannonball" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]