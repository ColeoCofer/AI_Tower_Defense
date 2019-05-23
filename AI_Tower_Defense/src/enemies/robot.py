import os
import random

import pygame
from projectile.projectile import DamageType

from .enemy import Enemy


class Robot(Enemy):
    numImages = 5

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 6
        self.health = self.maxHealth
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 8
        self.weaknesses = [DamageType.fire]

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/robot", "robot" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (64, 64)))
