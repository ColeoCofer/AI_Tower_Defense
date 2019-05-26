import os
import pygame
import random
import math
import enum
from .projectile import Projectile
from .projectile import DamageType

class RangeProjectile(Projectile):
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.animationCount = 0
        
    def fire(self):
        for weakness in self.targetEnemy.weaknesses:
            if self.damageType == weakness:
                break

    def draw(self, win):
        ''' Draws the enemy with given images '''
        numImages = len(self.images)
        self.image = self.images[self.animationCount // self.animationSpeed]
        
        #Iterate to the next animation image
        self.animationCount += 1
        
        #Reset the animation count if we rendered the last image
        if self.animationCount >= (numImages * self.animationSpeed):
            self.animationCount = 0

        #Display from center of character
        centerX = self.x - (self.width / 2)
        centerY = self.y - (self.height / 2)

        win.blit(self.image, (centerX, centerY))
        return self.move()


    def move(self):
        x1, y1 = self.towerPosition[0], self.towerPosition[1]
        x2, y2 = self.enemyStartingPosition[0], self.enemyStartingPosition[1]
        targetX, targetY = self.targetEnemy.x, self.targetEnemy.y

        ballEnemyDistance = math.sqrt((targetX - self.x)**2 + (targetY - self.y)**2)

        #Distance between current location and destination point
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        #Normalize the component vectors & add 20% of velocity
        dx = ((x2 - x1) / distance) * (self.velocity * 0.2)
        dy = ((y2 - y1) / distance) * (self.velocity * 0.2)

        self.x = self.x + dx
        self.y = self.y + dy

        return self.didHitEnemy(ballEnemyDistance)


    def didHitEnemy(self, distance):
        if distance < 30:
            self.explosiveDamage()
            self.resetRangeProjectile()
            return True


    def resetRangeProjectile(self):
        self.targetEnemy.hit(self.damage, self.damageType)
        self.x = self.towerPosition[0]
        self.y = self.towerPosition[1]

    def explosiveDamage(self):
        return