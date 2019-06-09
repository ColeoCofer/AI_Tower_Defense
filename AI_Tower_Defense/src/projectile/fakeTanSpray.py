import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class FakeTanSpray(Projectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 3                        # fake news does a lot of damage
        self.damageType = DamageType.fakeNews
        self.color = (200, 100, 50)
        self.reloadTime = 12                   # it can be spread quickly
        self.velocity = 15                      # it travels fast

        self.width = 97
        self.height = 100
        self.numImages = 1
        self.image = pygame.image.load("../assets/projectiles/fakenews/fakenews.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.images.append(self.image)

        self.animationCount = 0
        self.attackAnimationDuration = 10

    def draw(self, win, ticks, visualMode):
        if visualMode:
            ''' Draws the enemy with given images '''
            numImages = len(self.images)
            self.image = self.images[self.animationCount // self.animationSpeed]

            #Iterate to the next animation image
            self.animationCount += 1

            #Reset the animation count if we rendered the last image
            if self.animationCount >= (numImages * self.animationSpeed):
                self.animationCount = 0

            #Display from center of character
            centerX = self.x - (self.width / 2) + (self.width / 2) + 25
            centerY = self.y - self.height - 10

            win.blit(self.image, (centerX, centerY))
