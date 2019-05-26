import pygame
import os
import random
from .enemy import Enemy
from projectile.projectile import DamageType


class Zombie(Enemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 14
        self.health = self.maxHealth
        self.images = []
        self.numImages = 4
        self.velocity = 6
        self.healthBarYOffset = 30
        self.weaknesses.append(DamageType.fire)

        #Load animation images
        for i in range(self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/zombie", "zombie_" + str(i) + ".png"))
            self.images.append(image)
