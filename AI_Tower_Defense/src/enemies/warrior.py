import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.punch import Punch
from .enemy import Enemy
from .attackingEnemy import AttackingEnemy


class Warrior(AttackingEnemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.initialHealth = 16
        self.attackRadius = 30
        self.coinReward = 50
        self.startingHealth = self.initialHealth
        self.health = self.startingHealth
        self.velocity = random.randint(10,12)            # warriors are pretty fast
        self.weaknesses.append(DamageType.fire)
        self.weaknesses.append(DamageType.lightning)
        self.weaknesses.append(DamageType.poison)
        self.weaknesses.append(DamageType.lazer)        # warriors are weak to everything
        self.superWeakness = DamageType.fire            # and super weak to fire

        self.width = 80
        self.height = 80
        self.numImages = 20
        self.walkingImages = []
        self.attackingImages = []
        self.isAttacking = False
        self.animationSpeed = 2
        self.healthBarYOffset = 10

        self.spawnChance = 0.3
        self.spawnChanceLimit = 0.9

        #Load images
        for i in range(0, self.numImages):
            walkingImage = pygame.image.load(os.path.join("../assets/enemy/warrior/walk", "3_enemies_1_walk_" + str(i) + ".png"))
            self.walkingImages.append(pygame.transform.scale(walkingImage, (self.width, self.height)))

        for i in range(0, self.numImages + 1):
            attackImage = pygame.image.load(os.path.join("../assets/enemy/warrior/attack", "3_enemies_1_attack_" + str(i) + ".png"))
            self.attackingImages.append(pygame.transform.scale(attackImage, (self.width, self.height)))

        self.images = self.walkingImages

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
                    self.images = self.attackingImages

        return enemies


    # draw one of many awesome attacking enemies
    def draw(self, win, ticks, visualMode):
        if visualMode:
            #Since the attacking images have one more image than the walking images
            #If we are on the last attacking image, then we know we have finished the
            #attacking animation.
            if self.animationCount == (self.numImages):
                self.images = self.walkingImages
                self.isAttacking = False

            # check to see if enemy is frozen so as to display a snowman
            if self.frozen:
                self.image = self.snowman
            else:
                ''' Draws the enemy with given images '''
                # Set the image for # of frames ('//' means integer division)
                self.image = self.images[self.animationCount // self.animationSpeed]

                # Iterate to the next animation image
                self.animationCount += 1

                # Reset the animation count if we rendered the last image
                if self.animationCount >= (self.numImages * self.animationSpeed):
                    self.animationCount = 0

            # Display from center of character
            centerX = self.x - (self.width / 2)
            centerY = self.y - (self.height / 2)

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


    # overrides base class version
    def loadProjectile(self, enemy):
        return Punch((self.x, self.y), enemy, self.closeEnemies)
