import os
import pygame
from .animation import Animation

class Knight(Animation):

    def __init__(self, position):
        super().__init__(position)
        self.numImages = 10
        self.width = 70
        self.height = 70
        self.attackAnimationDuration = 25
        self.animationSpeed = 3
        self.animationCount = 0
        self.velocity = 0           

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/knight", "RedKnight_entity_000_basic attack 1_00" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]