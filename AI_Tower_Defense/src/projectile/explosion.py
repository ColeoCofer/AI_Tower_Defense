import os
import pygame
import random
import math
from .projectile import Projectile
from .projectile import DamageType

class Explosion():
    def __init__(self, position):
        self.numImages = 8
        self.width = 100
        self.height = 100
        self.attackAnimationDuration = 1200
        self.attackAnimationStopTime = 0
        self.animationSpeed = 3
        self.animationCount = 0
        self.velocity = 0
        self.images = []
        self.image = None
        self.x = position[0]
        self.y = position[1]

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/explosion", "explosion" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]

    def draw(self, win):
        ''' Draws the enemy with given images '''
        self.numImages = len(self.images)
        self.image = self.images[self.animationCount // self.animationSpeed]
        
        #Iterate to the next animation image
        self.animationCount += 1
        
        #Reset the animation count if we rendered the last image
        if self.animationCount >= (self.numImages * self.animationSpeed):
            self.animationCount = 0

        #Display from center of character
        centerX = self.x - (self.width / 2)
        centerY = self.y - (self.height / 2)

        win.blit(self.image, (centerX, centerY))