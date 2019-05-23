import pygame
import os
import random
from .enemy import Enemy

class Dino(Enemy):
    numImages = 10

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.health = 6
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 7
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/dino", "Walk (" + str(i) + ").png"))
            self.images.append(pygame.transform.scale(image, (64, 64)))
