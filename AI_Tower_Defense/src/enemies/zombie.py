import pygame
import os
import random
from .enemy import Enemy


class Zombie(Enemy):
    numImages = 4

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.health = 4
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        for i in range(self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/zombie", "zombie_" + str(i) + ".png"))
            #Uncomment to transform to different size
            #images.append(pygame.transform.scale(image, (64, 64)))
            self.images.append(image)
