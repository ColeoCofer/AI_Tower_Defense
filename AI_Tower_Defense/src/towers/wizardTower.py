import pygame
import os
import random
from .tower import Tower
from projectile.lazer import Lazer


class WizardTower(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.maxHealth = 100
        self.health = self.maxHealth
        self.attackRadius = 100
        self.coolDown = 3500
        self.damage = 4
        self.image = pygame.image.load(os.path.join("../assets/towers/wizard_tower/", "wizardTower.png"))
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.projectileColor = (10, 200, 200)

    def loadProjectile(self, enemy):
        laser = Lazer(self.position, enemy, self.closeEnemies)
        laser.color = self.projectileColor
        return laser