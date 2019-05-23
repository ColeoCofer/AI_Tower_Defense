import pygame
import math

ANIMATION_SPEED = 3 #Smaller numbers animate faster

class Enemy:
    def __init__(self, yOffset):
        images = []    #Animation images
        self.width = 64     #Image width
        self.height = 64    #Image height
        self.health = 2     #Default health
        self.velocity = 20   #Pixels per frame

        #List of coordinates that the enemy will follow
        self.pathIndex = 0
        self.path = [(-10, 443), (11, 433), (193, 429), (200, 206), (439, 203), (440, 504), (757, 506), (764, 366), (1196, 361), (1250, 361)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]

        #Slightly offset the y-axis
        for i in range(len(self.path)):
            self.path[i] = (self.path[i][0], self.path[i][1] + yOffset)

        self.animationCount = 0   #Keep track of which animation to display
        self.image = None         #Current image to render


    def draw(self, win):
        ''' Draws the enemy with given images '''
        numImages = len(self.images)

        #Set the image for # of frames ('//' means integer division)
        self.image = self.images[self.animationCount // ANIMATION_SPEED]

        #Iterate to the next animation image
        self.animationCount += 1

        #Reset the animation count if we rendered the last image
        if self.animationCount >= (numImages * ANIMATION_SPEED):
            self.animationCount = 0

        #Display from center of character
        centerX = self.x - (self.width / 2)
        centerY = self.y - (self.height / 2)

        win.blit(self.image, (centerX, centerY))
        self.move()


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
        x1, y1 = self.path[self.pathIndex]    #Current location of character
        numPathPositions = len(self.path)

        #Final point the char will move too
        finalX = self.path[numPathPositions-1][0]
        finalY = self.path[numPathPositions-1][1]

        #Check if we are at the end of the map
        if self.pathIndex + 1 >= numPathPositions:
            x2 = finalX + (self.width * 2) #Offset enough so they walk off the screen
            y2 = finalY
        else:
            x2, y2 = self.path[self.pathIndex + 1]

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
        if dx >= 0: #Moving right
            if dy >= 0: #Moving down
                if self.x >= x2 and self.y >= y2:
                    self.pathIndex += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.pathIndex += 1
        else:
            if dy >= 0: #Moving left
                if dy <= 0: #Moving up
                    if self.x <= x2 and self.y >= y2:
                        self.pathIndex += 1
                else:
                    if self.x <= x2 and self.y <= y2:
                        self.pathIndex += 1


    def hit(self, damage=1):
        ''' Returns true if the enemy died and subtracts damage from its health '''
        self.health -= damage
        if self.health <= 0:
            return True
