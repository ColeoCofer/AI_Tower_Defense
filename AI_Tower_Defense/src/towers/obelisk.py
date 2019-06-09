import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.fireBall import Fireball

class Obelisk(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.name = "Obelisk"
        self.startingHealth = 100                    # weak but with short range
        self.health = self.startingHealth
        self.weaknesses.append(DamageType.lightning)

        self.projectileColor = (100, 100, 100)
        self.image = pygame.image.load(os.path.join("../assets/towers/obelisk/", "obelisk.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    # overrides base class version
    def loadProjectile(self, enemy):
        fireball = Fireball(self.position, enemy, self.closeEnemies)
        return fireball
