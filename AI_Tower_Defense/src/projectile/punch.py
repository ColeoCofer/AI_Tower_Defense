import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class Punch(Projectile):
    
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 10                        # punches do a lot of damage, but are kind of slow
        self.damageType = DamageType.melee
        self.color = (200, 100, 50)
        self.reloadTime = 1000
        self.velocity = 5


    # TODO placeholder
    def draw(self, win):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-50, 50))

        color = tuple(newColor)