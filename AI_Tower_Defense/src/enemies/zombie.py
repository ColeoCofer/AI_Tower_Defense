import pygame
import os
import random
from .enemy import Enemy
from projectile.projectile import DamageType


class Zombie(Enemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 40                         # zombies are tough to kill
        self.health = self.maxHealth
        self.velocity = random.randint(2, 5)        # zombies are slow as hell
        self.weaknesses.append(DamageType.fire)     # zombies are only weak to fire, exploding, ice, and super weak to fire
        self.weaknesses.append(DamageType.lazer)     
        self.superWeakness = DamageType.fire        
        
        self.images = []
        self.numImages = 4
        self.healthBarYOffset = 30

        #Load animation images
        for i in range(self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/zombie", "zombie_" + str(i) + ".png"))
            self.images.append(image)
