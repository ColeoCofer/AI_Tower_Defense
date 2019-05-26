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
        self.projectilesFired = []
        self.projectileColor = (255, 255, 255)

        self.closeEnemies = []

    def attack(self, enemies, win):
        self.closeEnemies = enemies
        
        if self.frozen == False:
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
                    projectileToFire = self.loadProjectile(enemies[closestEnemyIndex])
                    projectileToFire.enemies = enemies
                    self.canAttackTime = ticks + projectileToFire.reloadTime
                    projectileToFire.attackAnimationStopTime = ticks + projectileToFire.attackAnimationDuration
                    projectileToFire.color = self.projectileColor
                    projectileToFire.fire()
                    self.projectilesFired.append(projectileToFire)  

        return enemies


    def draw(self, win):

        if self.frozen:
            self.image = self.snowman
        else:
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

        for i in range(len(self.projectilesFired)):
            if self.projectilesFired[i].attackAnimationStopTime < pygame.time.get_ticks():
                del self.projectilesFired[i]
                continue
            if self.projectilesFired[i].draw(win) == True:
                del self.projectilesFired[i]
            
                
            
        
        self.drawHealthBox(win, centerX, centerY)

        win.blit(self.image, (centerX, centerY))
        self.move()


    def loadProjectile(self, enemy):
        return Projectile((self.x, self.y), enemy)
