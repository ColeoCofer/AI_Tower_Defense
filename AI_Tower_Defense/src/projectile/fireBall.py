import pygame
import random
import os
from .rangeProjectile import RangeProjectile
from .projectile import DamageType
from animations.fireExplosion import FireExplosion

class Fireball(RangeProjectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 0                   # fire doesn't do a lot of damage
        self.damageType = DamageType.fire
        self.reloadTime = 750
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
        return FireExplosion(position)
