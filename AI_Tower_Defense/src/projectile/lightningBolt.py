import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class LightningBolt(Projectile):
    
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 4                             # do a lot of damage but slow reload
        self.damageType = DamageType.lightning
        self.color = (200, 100, 50)
        self.reloadTime = 1500
        self.velocity = 5


    # TODO placeholder
    def draw(self, win):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-50, 50))

        color = tuple(newColor)