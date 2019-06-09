import os
import pygame
import random
import math
import enum
from .projectile import Projectile
from .projectile import DamageType
from animations.animation import Animation


# base class for ranged projectiles
class RangeProjectile(Projectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.animationCount = 0
        self.detonationRange = 0
        self.attackAnimationDuration = 15
        self.attackRadius = 60                  # radius to take secondary damage on
        self.detonationRange = 75


    # only checks for weaknesses, ranges weapons only explode on contact so that is handled elsewhere
    def fire(self, ticks):
        for weakness in self.targetEnemy.weaknesses:
            if self.damageType == weakness:
                return True

        return False


    # draw a ranged weapon
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
            centerX = self.x - (self.width / 2)
            centerY = self.y - (self.height / 2)

            win.blit(self.image, (centerX, centerY))
            
        return self.move(ticks)


    # moves animation along
    def move(self, ticks):
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

        return self.didHitEnemy(ballEnemyDistance, ticks)


    # checks if we are close to enemy to do damage
    def didHitEnemy(self, distance, ticks):
        if distance < self.detonationRange:
            self.explosiveDamage(ticks)
            self.resetRangeProjectile(ticks)
            # TODO I think we should be returning something for informative
            return True


    # reset the center to the source tower if we hit the enemy
    def resetRangeProjectile(self, ticks):
        self.targetEnemy.hit(self.damage, self.damageType, ticks)
        self.x = self.towerPosition[0]
        self.y = self.towerPosition[1]


    # base class stub
    def explosiveDamage(self, ticks):
        return


    # base class stub
    def finalAnimation(self, position):
        return
