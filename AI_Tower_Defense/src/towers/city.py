import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.lazer import Lazer


class City(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.width = 350
        self.height = 350
        self.maxHealth = 10
        self.health = self.maxHealth
        self.attackRadius = 100
        self.coolDown = 1000
        self.damage = 1
        self.image = pygame.image.load(os.path.join("../assets/towers/final_city/", "city.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.weaknesses = [DamageType.lazer, DamageType.fire]
        self.projectile = Lazer(position)
