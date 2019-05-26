import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.fakeTanSpray import FakeTanSpray
from .enemy import Enemy
from .attackingEnemy import AttackingEnemy


class Trump(AttackingEnemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.maxHealth = 50                             # Trump is hard to kill
        self.health = self.maxHealth
        self.velocity = random.randint(3, 6)            # Trump is super slow
        self.weaknesses.append(DamageType.lazer)
        self.weaknesses.append(DamageType.fire)
        self.weaknesses.append(DamageType.lightning)    # Trump is weak to EVERYTHING
        self.superWeakness = DamageType.fire            # and super weak to fire

        self.animationSpeed = 1
        self.healthBarYOffset = 15
        self.images = []
        self.numImages = 20

        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/wizard", "2_enemies_1_walk_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))


    # overrides base class version
    def loadProjectile(self, enemy):
        return FakeTanSpray((self.x, self.y), enemy, self.closeEnemies)