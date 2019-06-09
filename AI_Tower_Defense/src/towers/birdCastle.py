import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.barrel import Barrel


class BirdCastle(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.name = "Bird Castle"
        self.startingHealth = 250                            # pretty tough
        self.health = self.startingHealth
        self.weaknesses.append(DamageType.lazer)
        self.weaknesses.append(DamageType.lightning)    # not weak to fire

        self.projectileColor = (100, 100, 100)

        self.image = pygame.image.load(os.path.join("../assets/towers/bird_castle/", "birdCastle.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    # overrides base class version
    def loadProjectile(self, enemy):
        barrel = Barrel(self.position, enemy, self.closeEnemies)
        barrel.color = self.projectileColor
        return barrel
