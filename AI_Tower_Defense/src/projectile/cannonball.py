import os
import pygame
import random
import math
from .projectile import Projectile
from .projectile import DamageType

class Cannonball(Projectile):
    def __init__(self, towerPosition, enemy):
        super().__init__(towerPosition, enemy)
        self.damage = 1
        self.damageType = DamageType.exploding
        self.reloadTime = 3000
        self.velocity = 100
        self.numImages = 1
        self.width = 30
        self.height = 30

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/cannonball", "cannonball" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]


    def draw(self, win):
        ''' Draws the enemy with given images '''
        # numImages = len(self.images)
        # self.image = self.images[self.animationCount // self.animationSpeed]
        #
        # #Iterate to the next animation image
        # self.animationCount += 1
        #
        # #Reset the animation count if we rendered the last image
        # if self.animationCount >= (numImages * self.animationSpeed):
        #     self.animationCount = 0

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
        # print(f"Distance {distance}")
        if distance < 30:
            self.resetCannonball()
            return True


    def resetCannonball(self):
        print("Reset cannoballllz")
        self.targetEnemy.hit(self.damage, self.damageType)
        self.x = self.towerPosition[0]
        self.y = self.towerPosition[1]

        # if dx > 0: #Moving right
        #
        #     if dy < 0: #Moving down
        #         if self.x >= x2 and self.y >= y2:
        #             self.resetCannonball()
        #     elif dy > 0:
        #         if self.x >= x2 and self.y <= y2:
        #             self.resetCannonball()
        #     else:
        #         #Not moving on y-axis
        #         if self.x >= x2:
        #             self.resetCannonball()
        #
        # elif dx < 0: #Moving left
        #     if dy < 0: #Moving down
        #         if self.x <= x2 and self.y >= y2:
        #             self.resetCannonball()
        #     elif dy > 0: #Moving up
        #         if self.x <= x2 and self.y <= y2:
        #             self.resetCannonball()
        #     else:
        #         #Not moving on y-axis
        #         if self.x <= x2:
        #             self.resetCannonball()
        # else: #Only moving on y-axis
        #     if dy < 0: #Moving down
        #         if self.y >= y2:
        #             self.resetCannonball()
        #     elif dy > 0: #Moving up
        #         if self.y <= y2:
        #             self.resetCannonball()
