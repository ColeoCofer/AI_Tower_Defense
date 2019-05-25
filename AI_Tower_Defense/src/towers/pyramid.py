import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType

class Pyramid(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.maxHealth = 10
        self.width = 80
        self.height = 80
        self.health = self.maxHealth
        self.attackRadius = 100
        self.coolDown = 1000
        self.damage = 1
        self.image = pygame.image.load(os.path.join("../assets/towers/pyramid/", "pyramid.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.weaknesses = [DamageType.lazer, DamageType.fire]
