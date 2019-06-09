import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.iceBeam import IceBeam


class Igloo(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.name = "Igloo"
        self.startingHealth = 80  # TODO change back
        self.health = self.startingHealth
        self.coolDown = 1000
        self.damage = 0
        self.weaknesses.append(DamageType.lazer)
        self.weaknesses.append(DamageType.fire)             # not weak to lightning

        self.projectileColor = (9, 146, 208)

        self.image = pygame.image.load(os.path.join("../assets/towers/igloo/", "igloo.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    # overrides base class version
    def loadProjectile(self, enemy):
        iceBeam =  IceBeam((self.position[0], self.position[1]), enemy, self.closeEnemies)
        iceBeam.color = self.projectileColor
        return iceBeam
