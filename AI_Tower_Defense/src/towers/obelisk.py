import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.lazer import Lazer


class Obelisk(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.maxHealth = 60                     # weak but with range
        self.health = self.maxHealth
        self.attackRadius = 200
        self.weaknesses.append(DamageType.lightning)
  
        self.projectileColor = (100, 100, 100)

        self.image = pygame.image.load(os.path.join("../assets/towers/obelisk/", "obelisk.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    # overrides base class version
    def loadProjectile(self, enemy):
        laser = Lazer(self.position, enemy, self.closeEnemies)
        laser.color = self.projectileColor
        return laser