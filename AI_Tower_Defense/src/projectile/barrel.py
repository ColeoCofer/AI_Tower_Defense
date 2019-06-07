import os
import pygame
import random
import math
from .projectile import DamageType
from .rangeProjectile import RangeProjectile
from animations.snakes import Snakes


class Barrel(RangeProjectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 12                        # barrels also do half this damage to the surroundings
        self.damageType = DamageType.poison     # barrels have snakes
        self.reloadTime = 30                    # reload time long
        self.velocity = 100                     # barrels are fast

        self.numImages = 4
        self.width = 40
        self.height = 40
        self.animationSpeed = 5

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/barrel", "barrel" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]


    # calulates the addtional surrounding damage
    def explosiveDamage(self, ticks):
        for enemy in self.enemies:
            dist = (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2
            #Use radius squared to avoid taking square roots of distance
            if dist <= self.attackRadius ** 2:
                halfDamage = self.damage / 2
                enemy.hit(halfDamage, self.damageType, ticks)
                self.damage += halfDamage


    # returns a residual animation
    def finalAnimation(self, position):
        return Snakes(position)
