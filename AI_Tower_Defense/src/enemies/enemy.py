import pygame

class Enemy:
    self.images = []    #Animation images

    def __init__(self, x, y width, height):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.health = 2           #Default health
        self.path = []            #List of coordinates that the enemy will follow
        self.animationCount = 0   #Keep track of which animation to display
        self.image = None

    def draw(self, win):
        ''' Draws the enemy with given images '''
        self.animationCount += 1                        #Iterate to the next animation image
        self.image = self.images[self.animationCount]   #Set the new image

        #Reset the animation count if we rendered the last image
        if self.animationCount >= len(self.images):
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
        ''' Moves the enemy closer to the next path coordinate '''
        pass

    def hit(self, damage=1):
        ''' Returns true if the enemy died and subtracts damage from its health '''
        self.health -= damage
        if self.health <= 0:
            return True
