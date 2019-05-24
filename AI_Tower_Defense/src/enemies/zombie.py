import pygame
import os
import random
from .enemy import Enemy
from projectile.projectile import DamageType


class Zombie(Enemy):
    numImages = 4

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 4
        self.health = self.maxHealth
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.healthBarYOffset = 30
        self.weaknesses = [DamageType.fire]

        #Load animation images
        for i in range(self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/zombie", "zombie_" + str(i) + ".png"))
            self.images.append(image)
