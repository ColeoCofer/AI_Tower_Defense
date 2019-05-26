import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.lightningBolt import LightningBolt
from .attackingEnemy import AttackingEnemy
from .enemy import Enemy

class Wizard(AttackingEnemy):
    numImages = 20

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 8
        self.health = self.maxHealth
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 1
        self.healthBarYOffset = 15
        self.weaknesses.append(DamageType.lazer)

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/wizard", "2_enemies_1_walk_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))

    def loadProjectile(self, enemy):
        return LightningBolt((self.x, self.y), enemy, self.closeEnemies)