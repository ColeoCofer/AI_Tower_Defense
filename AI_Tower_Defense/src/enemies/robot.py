import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.lazer import Lazer
from .enemy import Enemy
from .attackingEnemy import AttackingEnemy



class Robot(AttackingEnemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.initialHealth = 25                             # robots are tough
        self.startingHealth = self.initialHealth
        self.health = self.startingHealth
        self.velocity = random.randint(8, 11)            # robots are slow
        self.weaknesses.append(DamageType.fire)
        self.weaknesses.append(DamageType.lightning)    # robots are not weak to lasers
        self.superWeakness = DamageType.lightning       # they are super weak to lightning

        self.images = []
        self.projectileColor = (120, 70, 170)
        self.width = 54
        self.height = 54
        self.numImages = 3
        self.animationSpeed = 5
        self.healthBarYOffset = 5

        self.spawnChance = 0.4
        self.spawnChanceLimit = 0.85

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/robot", "robot" + str(i) + ".png"))
            image = pygame.transform.flip(image, True, False)
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))


    # overrides base classes version
    def loadProjectile(self, enemy):
        return Lazer((self.x, self.y), enemy, self.closeEnemies)
