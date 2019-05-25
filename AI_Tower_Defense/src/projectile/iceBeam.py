import pygame
import random
from .projectile import Projectile
from .projectile import DamageType

class IceBeam(Projectile):
    def __init__(self):
        super().__init__()
        self.damage = 0
        self.damageType = DamageType.ice
        self.color = (200, 100, 50)
        self.reloadTime = 500
        self.velocity = 5

    def draw(self, win, tower, enemy):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-50, 50))
        
        color = tuple(newColor)

        # need to add how projectiles are rendered
