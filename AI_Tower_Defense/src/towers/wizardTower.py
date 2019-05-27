import pygame
import os
import random
from .tower import Tower
from projectile.lazer import Lazer


class WizardTower(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.name = "Wizard Tower"
        self.cost = 400
        self.maxHealth = 350                # tough and long range
        self.health = self.maxHealth
        self.attackRadius = 350

        self.projectileColor = (150, 150, 150)

        self.image = pygame.image.load(os.path.join("../assets/towers/wizard_tower/", "wizardTower.png"))
        self.image = pygame.transform.scale(self.image, (120, 120))


    # overrides base class version
    def loadProjectile(self, enemy):
        laser = Lazer(self.position, enemy, self.closeEnemies)
        laser.color = self.projectileColor
        return laser
