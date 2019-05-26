import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.lazer import Lazer


class Obelisk(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.maxHealth = 30
        self.health = self.maxHealth
        self.attackRadius = 100
        self.coolDown = 1000
        self.damage = 1
        self.image = pygame.image.load(os.path.join("../assets/towers/obelisk/", "obelisk.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.weaknesses = [DamageType.lazer, DamageType.fire]
        # self.projectile = Lazer()

    def loadProjectile(self, enemy):
        return Lazer(self.position, enemy)