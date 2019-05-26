import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.cannonball import Cannonball

class SquareTower(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.maxHealth = 50
        self.health = self.maxHealth
        self.attackRadius = 250
        self.coolDown = 10000
        self.damage = 1
        self.image = pygame.image.load(os.path.join("../assets/towers/basic_castle/", "tower_square.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.weaknesses = [DamageType.lazer, DamageType.fire]
        # self.projectile = Cannonball()

    def loadProjectile(self, enemy):
        return Cannonball(self.position, enemy)
