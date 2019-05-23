import pygame
import os
import random
from .enemy import Enemy

class Dragon(Enemy):
    numImages = 4

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.health = 8
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/dragon", "dragon_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (64, 64)))
