import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType

class Igloo(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.width = 60
        self.height = 60
        self.maxHealth = 10
        self.health = self.maxHealth
        self.attackRadius = 150
        self.coolDown = 1000
        self.damage = 1
        self.image = pygame.image.load(os.path.join("../assets/towers/igloo/", "igloo.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.weaknesses = [DamageType.lazer, DamageType.fire]
