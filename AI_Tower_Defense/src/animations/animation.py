import os
import pygame
import random
import math


class Animation():

    def __init__(self, position):
        self.numImages = 0                  # all will get overridden except self.x and self.y
        self.width = 0
        self.height = 0
        self.attackAnimationDuration = 0
        self.attackAnimationStopTime = 0
        self.animationSpeed = 0
        self.animationCount = 0
        self.velocity = 0
        self.images = []
        self.image = None
        self.x = position[0]
        self.y = position[1]


    # draws an animation by frames
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
