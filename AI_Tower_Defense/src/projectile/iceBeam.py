import pygame
import random
from .projectile import Projectile
from .projectile import DamageType

class IceBeam(Projectile):
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 0
        self.damageType = DamageType.ice
        self.color = (9, 146, 208)
        self.reloadTime = 1250
        self.velocity = 5

    def draw(self, win):
        self.color = (9, 146, 208)
        color = tuple((self.color[0] + random.randint(-8, 45), self.color[1] + random.randint(-8,45), self.color[2] + random.randint(-8, 45)))
        pygame.draw.line(win, color, self.towerPosition, self.enemyStartingPosition, 5)
