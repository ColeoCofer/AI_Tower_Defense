import pygame
import math

HEALTH_GREEN = (255, 0, 0)
HEALTH_RED = (0,128,0)

class Enemy:
    def __init__(self, yOffset):
        self.maxHealth = 5
        self.health = self.maxHealth
        self.healthBarWidth = 50
        self.healthBarHeight = 10
        self.healthBarYOffset = 10   #Larger numbers will move the health bar closer to the enemies head
        self.velocity = 20           #Pixels per frame
        self.animationSpeed = 3      #Smaller numbers animate faster
        self.weaknesses = []

        #List of coordinates that the enemy will follow
        self.pathIndex = 0
        #self.path = [(-10, 443), (11, 433), (193, 429), (200, 206), (439, 203), (440, 504), (757, 506), (764, 366), (1196, 361), (1250, 361)]
        self.path = [(-5, 364), (17, 364), (183, 356), (215, 216), (338, 216), (381, 456), (553, 452), (585, 284), (730, 281), (757, 396), (897, 396), (920, 247), (1190, 246)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]

        #Slightly offset the y-axis
        # for i in range(len(self.path)):
        #     self.path[i] = (self.path[i][0], self.path[i][1] + yOffset)

        self.images = []          #Animation images
        self.width = 64           #Image width
        self.height = 64          #Image height
        self.animationCount = 0   #Keep track of which animation to display
        self.image = None         #Current image to render


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

        self.drawHealthBox(win, centerX, centerY)

        win.blit(self.image, (centerX, centerY))
        self.move()


    def drawHealthBox(self, win, centerX, centerY):
        ''' Draws a health box above each character '''
        if self.health > 0:
            healthBarX = self.x - (self.healthBarWidth / 2)
            healthBarY = self.y - self.height + self.healthBarYOffset
            if self.health == self.maxHealth:
                pygame.draw.rect(win, HEALTH_GREEN, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Outline of health bar
                pygame.draw.rect(win, HEALTH_RED, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Inside of health bar
            else:
                pygame.draw.rect(win, HEALTH_GREEN, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Outline health bar
                pygame.draw.rect(win, HEALTH_RED, (healthBarX, healthBarY, (self.healthBarWidth / self.maxHealth) * self.health, self.healthBarHeight))


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


    def hit(self, damage):
        ''' Returns true if the enemy died and subtracts damage from its health '''
        self.health = self.health - damage
