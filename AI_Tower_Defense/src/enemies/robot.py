import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.lazer import Lazer
from .enemy import Enemy
from .attackingEnemy import AttackingEnemy


class Robot(AttackingEnemy):
    numImages = 3

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.width = 54
        self.height = 54
        self.maxHealth = 12
        self.health = self.maxHealth
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 5
        self.weaknesses.append(DamageType.fire)
        self.projectileColor = (120, 70, 170)


        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/robot", "robot" + str(i) + ".png"))
            image = pygame.transform.flip(image, True, False)
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))

    def loadProjectile(self, enemy):
        return Lazer((self.x, self.y), enemy, self.closeEnemies)
