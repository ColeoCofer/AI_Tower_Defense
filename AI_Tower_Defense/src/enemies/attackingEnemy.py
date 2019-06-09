import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.projectile import Projectile
from .enemy import Enemy

# attacking enemy base class
class AttackingEnemy(Enemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.attackRadius = 150             # Distance it can attack enemies from
        self.canAttackTime = 0              # Timestamp showing when tower can attack again
        self.projectilesFired = []          # enemies projectile magazine
        self.projectileColor = (155, 155, 155)
        self.closeEnemies = []

        self.attackAnimationDuration = 2
        self.attackAnimationTimeStamp = 0

    # the enemy attacks!!
    def attack(self, enemies, ticks):
        self.closeEnemies = enemies

        # only thawed enemies can attack
        if self.frozen == False:
            '''
            Looks for enemies within it's attack radius
            Will find the closest one and attack it
            '''
            # Check if the tower is ready to attack again
            if ticks >= self.canAttackTime:
                attackableEnemies = []
                i = 0

                # TODO this is where we would need to be selective about what we add to the attack queue
                for enemy in enemies:
                    dist = (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2
                    # Use radius squared to avoid taking square roots of distance
                    if dist <= self.attackRadius ** 2:
                        attackableEnemies.append((i, dist))
                    i += 1

                if len(attackableEnemies) > 0:
                    # taget the closest enemy and load projectile into the magazine
                    closestEnemyIndex = (min(attackableEnemies, key = lambda enemy: enemy[1]))[0]
                    projectileToFire = self.loadProjectile(enemies[closestEnemyIndex])
                    projectileToFire.enemies = enemies
                    self.canAttackTime = ticks + projectileToFire.reloadTime
                    projectileToFire.attackAnimationStopTime = ticks + projectileToFire.attackAnimationDuration
                    projectileToFire.color = self.projectileColor
                    projectileToFire.fire(ticks)
                    self.projectilesFired.append(projectileToFire)

        return enemies


    # draw one of many awesome attacking enemies
    def draw(self, win, ticks, visualMode):
        if visualMode:
            # check to see if enemy is frozen so as to display a snowman
            if self.frozen:
                self.image = self.snowman
            else:
                ''' Draws the enemy with given images '''
                numImages = len(self.images)
                # Set the image for # of frames ('//' means integer division)
                self.image = self.images[self.animationCount // self.animationSpeed]

                # Iterate to the next animation image
                self.animationCount += 1

                # Reset the animation count if we rendered the last image
                if self.animationCount >= (numImages * self.animationSpeed):
                    self.animationCount = 0

            # Display from center of character
            centerX = self.x - (self.width / 2)
            centerY = self.y - (self.height / 2) + self.yOffset

            # draw health box, render sprite, and move sprite for next iteration
            self.drawHealthBox(win, centerX, centerY)
            win.blit(self.image, (centerX, centerY))


        # checks projectile magazine for projectiles to render
        i = 0
        while i < len(self.projectilesFired):
            # check and make sure animation time hasn't lapsed
            if self.projectilesFired[i].attackAnimationStopTime < ticks:
                del self.projectilesFired[i]
            # TODO I think we may want to think about this. It currently is saying that a projectile has hit it's target
            elif self.projectilesFired[i].draw(win, ticks, visualMode) == True:
                del self.projectilesFired[i]
            i += 1
        
        # self.move(ticks)


    # parent stub for loading projectiles
    def loadProjectile(self, enemy):
        return Projectile((self.x, self.y), enemy, self.closeEnemies)
