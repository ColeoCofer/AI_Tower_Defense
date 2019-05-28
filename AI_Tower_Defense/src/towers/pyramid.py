import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.lazer import Lazer


class Pyramid(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.name = "Pyramid"
        self.cost = 200
        self.maxHealth = 450                                # tough
        self.health = self.maxHealth
        self.attackRadius = 200
        self.weaknesses.append(DamageType.lightning)        # only weak to lightning and melee

<<<<<<< HEAD
        self.projectileColor = (200, 69, 50)
=======
        self.projectileColor = (150, 150, 150)
>>>>>>> 3763082b962a5a2c5af4c44e701e1bf8a9064b11
        self.width = 80
        self.height = 80
        self.healthBarYOffset = 30

        self.image = pygame.image.load(os.path.join("../assets/towers/pyramid/", "pyramid.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    # overrides base class version
    def loadProjectile(self, enemy):
        laser = Lazer(self.position, enemy, self.closeEnemies)
        laser.color = self.projectileColor
        return laser
