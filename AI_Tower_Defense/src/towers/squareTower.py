import pygame
import os
import random
from .tower import Tower
from projectile.projectile import DamageType
from projectile.cannonball import Cannonball


class SquareTower(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.name = "Cannon Castle"
        self.startingHealth = 250                            # tough with cannnonballs
        self.health = self.startingHealth
        self.weaknesses.append(DamageType.lazer)        # impervious to fire
        self.weaknesses.append(DamageType.lightning)

        self.projectileColor = (100, 100, 100)

        self.image = pygame.image.load(os.path.join("../assets/towers/basic_castle/", "tower_square.png"))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    # overrides base class version
    def loadProjectile(self, enemy):
        ball = Cannonball(self.position, enemy, self.closeEnemies)
        ball.color = self.projectileColor
        return ball
