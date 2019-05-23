import pygame
import os
from .enemy import Enemy

class Dino(Enemy):
    numImages = 10

    def __init__(self, velocity, yOffset):
        super().__init__(yOffset)

        self.images = []
        self.velocity = velocity
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/dino", "Walk (" + str(i) + ").png"))
            self.images.append(pygame.transform.scale(image, (64, 64)))
