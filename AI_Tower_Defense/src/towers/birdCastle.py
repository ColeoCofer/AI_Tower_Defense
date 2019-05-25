import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.lazer import Lazer


class BirdCastle(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.maxHealth = 150
        self.health = self.maxHealth
        self.attackRadius = 100
        self.coolDown = 1000
        self.damage = 1
        self.image = pygame.image.load(os.path.join("../assets/towers/bird_castle/", "birdCastle.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.weaknesses = [DamageType.lazer, DamageType.fire]
        self.projectile = Lazer(position)
