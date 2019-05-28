import pygame
import random
import os
from .rangeProjectile import RangeProjectile
from .projectile import DamageType
from animations.explosion import Explosion

class Fireball(RangeProjectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 2                   # fire doesn't do a lot of damage
        self.damageType = DamageType.fire
        self.reloadTime = 1500
        self.velocity = 100
        self.attackRadius = 40
        self.detonationRange = 30
        self.numImages = 8
        self.width = 30
        self.height = 30
        self.attackAnimationDuration = 5000

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/fireBall", "fireBall" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]

    def finalAnimation(self, position):
        return Explosion(position)
