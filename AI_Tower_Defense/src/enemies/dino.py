import os
import random
import pygame
from projectile.projectile import DamageType
from .enemy import Enemy


class Dino(Enemy):

    spawnChance = 0.4
    spawnChanceLimit = 0.8
    startingHealth = 20                             # Dino's are tough
    velocity = 16  # random.randint(5, 8)            # Dino's are slow

    def __init__(self, yOffset):
        super().__init__(yOffset)
        # self.startingHealth = 20                             # Dino's are tough
        self.health = self.startingHealth
        # self.velocity = random.randint(5, 8)            # Dino's are slow
        self.weaknesses.append(DamageType.lazer)
        self.weaknesses.append(DamageType.fire)
        self.weaknesses.append(DamageType.poison)
        self.weaknesses.append(DamageType.lightning)    # Dino's are weak to everything
        self.superWeakness = None                       # but not super weak to anything

        self.numImages = 11
        self.animationSpeed = 7
        self.healthBarYOffset = 15
        self.images = []

        # self.spawnChance = 0.4
        # self.spawnChanceLimit = 0.8

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/dino", "Walk (" + str(i) + ").png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
