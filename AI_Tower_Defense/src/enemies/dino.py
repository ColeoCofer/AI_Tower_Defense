import os
import random
import pygame
from projectile.projectile import DamageType
from .enemy import Enemy


class Dino(Enemy):
    numImages = 10

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 6
        self.health = self.maxHealth
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 7
        self.healthBarYOffset = 15
        self.weaknesses.append(DamageType.lazer)

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/dino", "Walk (" + str(i) + ").png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
