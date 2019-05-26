import os
import random
import pygame
from projectile.projectile import DamageType
from .attackingEnemy import AttackingEnemy
from .enemy import Enemy
from projectile.fakeTanSpray import FakeTanSpray


class Trump(AttackingEnemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 50
        self.health = self.maxHealth
        self.images = []
        self.numImages = 20
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 1
        self.healthBarYOffset = 15
        self.weaknesses.append(DamageType.lazer, DamageType.fire, DamageType.exploding, DamageType.lightning)
        self.projectile = FakeTanSpray((0,0), Enemy(0))

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/wizard", "2_enemies_1_walk_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))

    def loadProjectile(self, enemy):
        return FakeTanSpray((self.x, self.y), enemy, self.closeEnemies)