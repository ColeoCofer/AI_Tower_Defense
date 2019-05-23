import pygame
import os
import random
from .tower import Tower


class SquareTower(Tower):

    def __init__(self, position):
        super().__init__(position)
        self.health = 10
        self.attackRadius = 100
        self.coolDown = 1000
        self.damage = 1
        self.image = pygame.image.load(os.path.join("../assets/towers/basic_castle/", "tower_square.png"))
        self.image = pygame.transform.scale(self.image, (64, 64))
