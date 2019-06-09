import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class Lazer(Projectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 2                         # lazers do medium damage and fire quickly
        self.damageType = DamageType.lazer
        self.color = (200, 100, 50)
        self.reloadTime = 4
        self.velocity = 5


    # draws a simple line
    def draw(self, win, ticks, visualMode):
        if visualMode:
            newColor = []
            for channel in self.color:
                newColor.append(channel + random.randint(-50, 50))
            color = tuple(newColor)
            pygame.draw.line(win, color, self.towerPosition, (self.targetEnemy.x, self.targetEnemy.y), 5)
