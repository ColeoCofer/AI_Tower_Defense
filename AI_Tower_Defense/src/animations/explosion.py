import os
import pygame
from .animation import Animation

class Explosion(Animation):

    def __init__(self, position):
        super().__init__(position)
        self.numImages = 8
        self.width = 100
        self.height = 100
        self.attackAnimationDuration = 15
        self.animationSpeed = 3
        self.animationCount = 0
        self.velocity = 0           # explosions are stationary

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/explosion", "explosion" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]
