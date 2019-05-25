import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType

class SquareTower(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.maxHealth = 10
        self.health = self.maxHealth
        self.attackRadius = 150
        self.coolDown = 1000
        self.damage = 1
        self.image = pygame.image.load(os.path.join("../assets/towers/basic_castle/", "tower_square.png"))
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.weaknesses = [DamageType.lazer, DamageType.fire]
