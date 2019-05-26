import pygame
import random
from .projectile import Projectile
from .projectile import DamageType

class Punch(Projectile):
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 10
        self.damageType = DamageType.melee
        self.color = (200, 100, 50)
        self.reloadTime = 500
        self.velocity = 5

    def draw(self, win):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-50, 50))

        color = tuple(newColor)

