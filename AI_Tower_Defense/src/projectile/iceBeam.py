import pygame
import random
from .projectile import Projectile
from .projectile import DamageType

class IceBeam(Projectile):
    def __init__(self, position):
        super().__init__(position)
        self.damage = 0
        self.damageType = DamageType.ice
        self.color = (8, 146, 208)
        self.reloadTime = 1250
        self.velocity = 5

    def draw(self, win, tower, enemy):
        color = tuple((self.color[0] + random.randint(-8, 45), self.color[1] + random.randint(-8,45), self.color[2] + random.randint(-8, 45)))
        pygame.draw.line(win, color, tower, enemy, 5)
