import pygame
import math
import os
from projectile.projectile import DamageType
from constants.animationConstants import *


# enemy base class
class Enemy:

    def __init__(self, yOffset):
        self.initialHealth = 5                   # Amt of health at level 1
        self.startingHealth = self.initialHealth # Starting health at each level (it increments after x number of levels go by)
        self.health = self.startingHealth        # Current health
        self.levelHealth = 0
        self.coinReward = 5
        self.velocity = 0
        self.weaknesses = [DamageType.ice, DamageType.exploding, DamageType.melee]      # all creatures are weak to ice, explosions, and melee
        self.superWeakness = None   # will cause an enemy to lose 2x damage when projectile damage is the same
        self.frozen = False
        self.frozenDuration = 0

        # Animation
        self.animationSpeed = 3      # Smaller numbers animate faster
        self.images = []             # Animation images
        self.width = 64              # Base Image width
        self.height = 64             # Base Image height
        self.animationCount = 0      # Keep track of which animation to display
        self.image = None            # Current image to render
        self.healthBarWidth = 50
        self.healthBarHeight = 10
        self.healthBarYOffset = 2    #Larger numbers will move the health bar closer to the enemies head
        self.numImages = 0
        self.yOffset = yOffset

        #Spawn
        self.spawnChance = 0.5        #Default starting chance of being spawned
        self.spawnChanceLimit = 0.8   #Maximum limit that an enemy's spawn chance will be

        # default snowman animation
        self.snowman = pygame.transform.scale(pygame.image.load(os.path.join("../assets/enemy/snowman", "snowman.png")), (self.width, self.height))

        # List of coordinates that the enemy will follow
        self.pathIndex = 0
        self.path = ENEMY_PATH
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path.append((1250 + (self.width * 2), self.path[-1][1]))


    def draw(self, win, ticks, visualMode):
        if visualMode:
            # if the enemy is frozen display snowman
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

            # draw health box, render sprite, and move
            self.drawHealthBox(win, centerX, centerY)
            win.blit(self.image, (centerX, centerY))
        # self.move()


    def drawHealthBox(self, win, centerX, centerY):
        ''' Draws a health box above each character '''
        if self.health > 0:
            healthBarX = self.x - (self.healthBarWidth / 2)
            healthBarY = centerY - (self.height / 2) + (self.healthBarYOffset)
            if self.health == self.levelHealth:
                pygame.draw.rect(win, HEALTH_GREEN, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Outline of health bar
                pygame.draw.rect(win, HEALTH_RED, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight))   #Inside of health bar
            else:
                pygame.draw.rect(win, HEALTH_GREEN, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Outline health bar
                pygame.draw.rect(win, HEALTH_RED, (healthBarX, healthBarY, (self.healthBarWidth / self.startingHealth) * self.health, self.healthBarHeight))


    def collide(self, col_x, col_y):
        ''' Returns true if the coordinate has hit the enemy '''
        if col_x <= self.x + self.width and col_x >= self.x:
            if col_y <= self.y + self.height and col_y >= self.y:
                return True
        return False


    def move(self, ticks):
        if self.frozen:
            if self.frozenDuration < ticks:
                self.frozen = False
        else:
            '''
            Moves the enemy closer to the next path coordinate.
            Uses the slope between the current position and the next position.
            '''
            x1, y1 = self.path[self.pathIndex]      #Current location of character

            if self.pathIndex < len(self.path):
                x2, y2 = self.path[self.pathIndex + 1]  #Destination location

            #Distance between current location and destination point
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            #Normalize the component vectors & add 20% of velocity
            dx = ((x2 - x1) / distance) * (self.velocity * 0.2)
            dy = ((y2 - y1) / distance) * (self.velocity * 0.2)

            self.x = self.x + dx
            self.y = self.y + dy

            self.didPassPoint(x2, y2, dx, dy)


    def didPassPoint(self, x2, y2, dx, dy):
        '''
        Increments the pathIndex if the enemy passes the next point.
        First checks for the direction that the enemy is walking in,
        and then if it surpassed the next point on the appropriate axis.
        Note: pyGame axis starts from the top left corner
        '''
        if dx > 0: #Moving right
            if dy > 0: #Moving down
                if self.x >= x2 and self.y >= y2:
                    self.pathIndex += 1
            elif dy < 0: #Moving up
                if self.x >= x2 and self.y <= y2:
                    self.pathIndex += 1
            else: #Not moving on y-axis
                if self.x >= x2:
                    self.pathIndex += 1
        elif dx < 0: #Moving left
            if dy > 0: #Moving down
                if self.x <= x2 and self.y >= y2:
                    self.pathIndex += 1
            elif dy < 0: #Moving up
                if self.x <= x2 and self.y <= y2:
                    self.pathIndex += 1
            else: #Not moving on y-axis
                if self.x <= x2:
                    self.pathIndex += 1
        else: #Not moving on x-axis
            if dy > 0 and self.y >= y2: #Moving down
                self.pathIndex += 1
            elif dy < 0 and self.y <= y2: #Moving up
                self.pathIndex += 1


    def hit(self, damage, damageType, ticks):
        ''' Returns true if the enemy died and subtracts damage from its health '''
        if damageType == self.superWeakness:
            damage *= 2
        self.health = self.health - damage
        if damageType == DamageType.ice:
            self.frozen = True
            self.frozenDuration = ticks + FROZEN_DURATION
