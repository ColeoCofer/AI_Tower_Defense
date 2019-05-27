import pygame
import random
import os
from .projectile import Projectile
from .projectile import DamageType


class Punch(Projectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 5                        # punches do a lot of damage, but are kind of slow
        self.damageType = DamageType.melee
        self.color = (200, 100, 50)
        self.reloadTime = 1000
        self.velocity = 5
        self.numImages = 1
        self.width = 35
        self.height = 35
        self.attackAnimationDuration = 400

        # for i in range(0, self.numImages):
        #     image = pygame.image.load(os.path.join("../assets/projectiles/punch", "fist" + str(i) + ".png"))
        #     self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        # self.image = self.images[0]

    # draw a ranged weapon
    def draw(self, win):
        pass
        # ''' Draws the enemy with given images '''
        # numImages = len(self.images)
        # self.image = self.images[self.animationCount // self.animationSpeed]
        #
        # #Iterate to the next animation image
        # self.animationCount += 1
        #
        # #Reset the animation count if we rendered the last image
        # if self.animationCount >= (numImages * self.animationSpeed):
        #     self.animationCount = 0
        #
        # #Display from center of character
        # centerX = self.x - (self.width / 2) + self.width
        # centerY = self.y - (self.height / 2)
        #
        # win.blit(self.image, (centerX, centerY))
