import pygame
import os
import random
from .enemy import Enemy

class Robot(Enemy):
    numImages = 5

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.health = 6
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 8
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/robot", "robot" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (64, 64)))
