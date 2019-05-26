import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class Fireball(Projectile):
    
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 5                     # fire doesn't do a lot of damage
        self.damageType = DamageType.fire   
        self.color = (200, 100, 50)
        self.reloadTime = 750               # fire can be flung quickly    
        self.velocity = 7       


    # TODO placeholder
    def draw(self, win):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-50, 50))

        color = tuple(newColor)