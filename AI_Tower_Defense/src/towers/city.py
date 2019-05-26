import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.lazer import Lazer


class City(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.maxHealth = 1500
        self.health = self.maxHealth
        self.attackRadius = 150
        self.weaknesses.append(DamageType.lazer)            # weak to everything but she is super buff
        self.weaknesses.append(DamageType.fire)
        self.weaknesses.append(DamageType.lightning)
        
        self.projectileColor = (200, 200, 200)
        self.width = 250
        self.height = 250
        
        self.image = pygame.image.load(os.path.join("../assets/towers/final_city/", "city.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    # overrides basae class version
    def loadProjectile(self, enemy):
        laser = Lazer(self.position, enemy, self.closeEnemies)
        laser.color = self.projectileColor
        return laser
