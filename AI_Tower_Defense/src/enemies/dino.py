import os
import random
import pygame
from projectile.projectile import DamageType
from .enemy import Enemy


class Dino(Enemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 20                   # Dino's are tough
        self.health = self.maxHealth
        self.velocity = random.randint(3, 5)  # Dino's are slow
        self.weaknesses.append(DamageType.lazer)
        self.weaknesses.append(DamageType.fire)
        self.weaknesses.append(DamageType.lightning)    # Dino's are weak to everything
        
        self.numImages = 10
        self.animationSpeed = 7
        self.healthBarYOffset = 15
        self.images = []

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/dino", "Walk (" + str(i) + ").png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
