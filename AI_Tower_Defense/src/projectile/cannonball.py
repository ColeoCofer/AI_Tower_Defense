import os
import pygame
import random
import math
from .projectile import DamageType
from .rangeProjectile import RangeProjectile
from animations.explosion import Explosion


class Cannonball(RangeProjectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 4                         # cannonballs also do half this damage to the surroundings
        self.damageType = DamageType.exploding  # cannonballs go boom
        self.reloadTime = 3000                  # reload time long
        self.velocity = 100                     # cannonballs are fast
        self.attackRadius = 40                  # radius to take secondary damage on
        self.detonationRange = 30

        self.numImages = 4
        self.width = 30
        self.height = 30
        self.attackAnimationDuration = 5000

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/cannonball", "cannonball" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]


    # calulates the addtional surrounding damage
    def explosiveDamage(self):
        for enemy in self.enemies:
            dist = (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2
            #Use radius squared to avoid taking square roots of distance
            if dist <= self.attackRadius ** 2:
                enemy.hit((self.damage / 2), self.damageType)


    # returns a residual animation
    def finalAnimation(self, position):
        return Explosion(position)
