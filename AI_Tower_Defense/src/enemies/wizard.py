import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.lightningBolt import LightningBolt
from .enemy import Enemy
from .attackingEnemy import AttackingEnemy


class Wizard(AttackingEnemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.initialHealth = 12                         # wizards are kind of squishy
        self.startingHealth = self.initialHealth
        self.health = self.startingHealth
        self.coinReward = 25
        self.velocity = random.randint(9, 13)       # wizards are fast as hell
        self.weaknesses.append(DamageType.lazer)
        self.weaknesses.append(DamageType.poison)
        self.weaknesses.append(DamageType.fire)     # wizards are not weak to lightning
        self.superWeakness = DamageType.exploding   # and super weak to exploding shells

        self.images = []
        self.animationSpeed = 1
        self.numImages = 20
        self.healthBarYOffset = 15

        self.spawnChance = 0.4
        self.spawnChanceLimit = 0.7

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/wizard", "2_enemies_1_walk_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))


    # overrides base class version
    def loadProjectile(self, enemy):
        return LightningBolt((self.x, self.y), enemy, self.closeEnemies)
