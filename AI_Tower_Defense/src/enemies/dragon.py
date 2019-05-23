import pygame
import os
import random
from .enemy import Enemy

class Dragon(Enemy):
    numImages = 4

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 8
        self.health = self.maxHealth
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 5
        self.healthBarYOffset = 30

        #Load animation images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/dragon", "dragon_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (64, 64)))
