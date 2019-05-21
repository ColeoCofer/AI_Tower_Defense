import pygame
import math

class Enemy:
    images = []    #Animation images

    def __init__(self):
        self.width = 64     #Image width
        self.height = 64    #Image height
        self.health = 2     #Default health
        self.velocity = 5   #Pixels per frame

        #List of coordinates that the enemy will follow
        self.path = [(0, 437), (192, 430), (198, 203), (440, 207), (440, 508), (756, 504), (764, 364), (1192, 361), (1250, 361)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]

        self.pathIndex = 0
        self.moveCount = 0
        self.distanceMoved = 0

        self.animationCount = 0   #Keep track of which animation to display
        self.image = None         #Current image to render


    def draw(self, win):
        ''' Draws the enemy with given images '''
        numImages = len(self.images)
        self.image = self.images[self.animationCount // 3]   #Set the new image
        self.animationCount += 1                        #Iterate to the next animation image

        #Reset the animation count if we rendered the last image
        if self.animationCount >= (numImages * 3):
            self.animationCount = 0

        win.blit(self.image, (self.x, self.y))          #Update the image
        self.move()                                     #Move the player after displaying


    def collide(self, col_x, col_y):
        ''' Returns true if the coordinate has hit the enemy '''
        if col_x <= self.x + self.width and col_x >= self.x:
            if col_y <= self.y + self.height and col_y >= self.y:
                return True
        return False


    def move(self):
        '''
        Moves the enemy closer to the next path coordinate.
        Uses the slope between the current position and the next position.
        '''
        x1, y1 = self.path[self.pathIndex]
        numPathPositions = len(self.path)
        maxWidth = self.path[numPathPositions-1][0]
        finalHeight = self.path[numPathPositions-1][1]

        #Check if we are at the end of the map
        if self.pathIndex + 1 >= numPathPositions:
            x2 = maxWidth + (self.width * 2) #Offset enough so they walk off the screen
            y2 = finalHeight
        else:
            x2, y2 = self.path[self.pathIndex + 1]

        distanceToNextPoint = math.sqrt((x2-x1)**2 + (y2-y1)**2)

        #Take another step towards the point
        self.moveCount += 1

        #Slope from current point to the next point
        pathSlope =  (x2 - x1, y2 - y1)

        #Calculate distance to move in each direction
        dx = self.x + pathSlope[0] * self.moveCount
        dy = self.y + pathSlope[1] * self.moveCount

        #We passed the point we are moving to
        if self.distanceMoved >= distanceToNextPoint:
            self.distanceMoved = 0
            self.moveCount = 0
            self.pathIndex += 1      #Target the next point

            if self.pathIndex >= numPathPositions:
                return False

        self.x = dx
        self.y = dy

        return True


    def hit(self, damage=1):
        ''' Returns true if the enemy died and subtracts damage from its health '''
        self.health -= damage
        if self.health <= 0:
            return True
