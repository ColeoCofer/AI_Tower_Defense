import os
import random

import pygame
from projectile.projectile import DamageType
from projectile.projectile import Projectile


from .enemy import Enemy


class AttackingEnemy(Enemy):
    numImages = 5

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.attackRadius = 150  #Distance it can attach enemies from
        self.canAttackTime = 0 #Timestamp showing when tower can attack again
        self.attackAnimationDuration = 200
        self.attackAnimationTimeStamp = 0
        self.enemiesBeingAttacked = []
        self.projectile = Projectile()

    def attack(self, enemies, win):
        '''
        Looks for enemies within it's attack radius
        Will find the closest one and attack it
        '''
        #Check if the tower is ready to attack again
        ticks = pygame.time.get_ticks()
        if ticks >= self.canAttackTime:
            attackableEnemies = []
            i = 0

            # TODO this is where we would need to be selective about what we add to the attack queue
            for enemy in enemies:
                dist = (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2
                #Use radius squared to avoid taking square roots of distance
                if dist <= self.attackRadius ** 2:
                    attackableEnemies.append((i, dist))
                i += 1

            if len(attackableEnemies) > 0:
                closestEnemyIndex = (min(attackableEnemies, key = lambda enemy: enemy[1]))[0]
                self.attackAnimationTimeStamp = ticks + self.attackAnimationDuration

                enemyX, enemyY = enemies[closestEnemyIndex].x, enemies[closestEnemyIndex].y
                self.enemiesBeingAttacked.append((enemyX, enemyY))
                self.projectile.fire(enemies[closestEnemyIndex])
                self.canAttackTime = ticks + self.projectile.reloadTime

        return enemies


    def draw(self, win):
        ''' Draws the enemy with given images '''
        numImages = len(self.images)

        #Set the image for # of frames ('//' means integer division)
        self.image = self.images[self.animationCount // self.animationSpeed]

        #Iterate to the next animation image
        self.animationCount += 1

        #Reset the animation count if we rendered the last image
        if self.animationCount >= (numImages * self.animationSpeed):
            self.animationCount = 0

        #Display from center of character
        centerX = self.x - (self.width / 2)
        centerY = self.y - (self.height / 2)

        #Check if we should display the attack animation
        if pygame.time.get_ticks() <= self.attackAnimationTimeStamp:
            for enemy in self.enemiesBeingAttacked:
                self.projectile.draw(win, (self.x, self.y), enemy)
        else:
            self.enemiesBeingAttacked = []

        self.drawHealthBox(win, centerX, centerY)

        win.blit(self.image, (centerX, centerY))
        self.move()