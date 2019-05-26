import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.iceBeam import IceBeam


class Igloo(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.width = 60
        self.height = 60
        self.maxHealth = 90
        self.health = self.maxHealth
        self.attackRadius = 250
        self.coolDown = 1000
        self.damage = 0
        self.image = pygame.image.load(os.path.join("../assets/towers/igloo/", "igloo.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.weaknesses = [DamageType.lazer, DamageType.fire]
        # self.projectile = IceBeam(position)

    def loadProjectile(self, enemy):
        return IceBeam(self.position, enemy)
