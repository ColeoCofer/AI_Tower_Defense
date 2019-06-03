import pygame
import random
import os
from .rangeProjectile import RangeProjectile
from .projectile import DamageType
from animations.disintegrate import Disintegrate


class LightningBolt(RangeProjectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 7                             # do a lot of damage but slow reload
        self.damageType = DamageType.lightning
        self.reloadTime = 25
        self.velocity = 80                     # cannonballs are fast

        self.numImages = 14
        self.width = 80
        self.height = 80
        self.animationSpeed = 2

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/lightning", "Explosion_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]


    # returns a residual animation
    def finalAnimation(self, position):
        return Disintegrate(position)
