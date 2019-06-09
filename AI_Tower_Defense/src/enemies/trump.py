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
        self.initialHealth = 50                        # Trump is hard to kill
        self.startingHealth = self.initialHealth
        self.health = self.startingHealth
        self.coinReward = 100
        self.attackRadius = 125
        self.velocity = random.randint(5, 8)            # Trump is super slow
        self.weaknesses.append(DamageType.lazer)
        self.weaknesses.append(DamageType.fire)
        self.weaknesses.append(DamageType.poison)
        self.weaknesses.append(DamageType.lightning)    # Trump is weak to EVERYTHING
        self.superWeakness = DamageType.poison          # and super weak to fire

        self.healthBarYOffset = 20
        self.width = 100
        self.height = 100
        self.images = []
        self.numImages = 2
        self.animationSpeed = 10

        self.spawnChance = 0.01
        self.spawnChanceLimit = 0.04

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/trump", "trump" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))


    # overrides base class version
    def loadProjectile(self, enemy):
        return FakeTanSpray((self.x, self.y), enemy, self.closeEnemies)
