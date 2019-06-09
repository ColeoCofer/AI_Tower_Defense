import pygame
import os
import random
from .enemy import Enemy
from projectile.projectile import DamageType


class Zombie(Enemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.initialHealth = 40                         # zombies are tough to kill
        self.coinReward = 20
        self.startingHealth = self.initialHealth
        self.health = self.startingHealth
        self.velocity = random.randint(5, 8)        # zombies are slow as hell
        self.weaknesses.append(DamageType.fire)     # zombies are only weak to fire, exploding, ice, and super weak to fire
        self.weaknesses.append(DamageType.lazer)
        self.superWeakness = DamageType.fire

        self.images = []
        self.numImages = 4
        self.healthBarYOffset = 30

        self.spawnChance = 0.6
        self.spawnChanceLimit = 0.7

        #Load animation images
        for i in range(self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/zombie", "zombie_" + str(i) + ".png"))
            self.images.append(image)
