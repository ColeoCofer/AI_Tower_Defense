import pygame
import os
import random
from .tower import Tower


class WizardTower(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.health = 45
        self.attackRadius = 100
        self.coolDown = 3500
        self.damage = 4
        self.image = pygame.image.load(os.path.join("../assets/towers/wizard_tower/", "wizardTower.png"))
        self.image = pygame.transform.scale(self.image, (64, 64))
