import os
import pygame
from .animation import Animation

class Disintegrate(Animation):

    def __init__(self, position):
        super().__init__(position)
        self.numImages = 9
        self.width = 100
        self.height = 100
        self.attackAnimationDuration = 15
        self.animationSpeed = 2
        self.animationCount = 0
        self.velocity = 0           # explosions are stationary

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/disintegrate", "hit_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]