import pygame
import random
from .projectile import Projectile
from .projectile import DamageType

class LightningBolt(Projectile):
    def __init__(self, position):
        super().__init__(position)
        self.damage = 7
        self.damageType = DamageType.lightning
        self.color = (200, 100, 50)
        self.reloadTime = 1000
        self.velocity = 5

    def draw(self, win, tower, enemy):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-50, 50))

        color = tuple(newColor)

        # need to add how projectiles are rendered
