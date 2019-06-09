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
        self.startingHealth = 450                                # tough
        self.health = self.startingHealth
        self.weaknesses.append(DamageType.lightning)
        self.projectileColor = (200, 69, 50)
        self.healthBarYOffset = 30

        self.image = pygame.image.load(os.path.join("../assets/towers/pyramid/", "pyramid.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    # overrides base class version
    def loadProjectile(self, enemy):
        laser = Lazer(self.position, enemy, self.closeEnemies)
        laser.color = self.projectileColor
        return laser
