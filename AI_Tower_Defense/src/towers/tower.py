import pygame

class Tower:
    def __init__(self, position):
        self.x = position[0]   #Position on map
        self.y = position[1]
        self.damage = 0        #Amount of damage delt per attack
        self.attackRate = 0    #Times the tower can attack per second
        self.attackRadius = 0  #Distance it can attach enemies from
        self.image = None      #Current image being displayed
        self.width = 64        #Width of animation images
        self.height = 64       #Height of animation images


    def attach(self):
        pass

    def draw(self, win):
        centerX = self.x - (self.width / 2)
        centerY = self.y - (self.height / 2)
        win.blit(self.image, (centerX, centerY))
