import os
import pygame
import random
import math
from .rangeProjectile import RangeProjectile
from .projectile import DamageType

class Cannonball(RangeProjectile):
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 2
        self.damageType = DamageType.exploding
        self.reloadTime = 3000
        self.velocity = 100
        self.numImages = 5
        self.width = 30
        self.height = 30
        self.attackAnimationDuration = 10000
        self.attackRadius = 30
        self.animationSpeed = 4

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/cannonball", "cannonball" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]

    def explosiveDamage(self):
        for enemy in self.enemies:
            dist = (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2
            #Use radius squared to avoid taking square roots of distance
            if dist <= self.attackRadius ** 2:
                enemy.hit((self.damage / 2), self.damageType)
