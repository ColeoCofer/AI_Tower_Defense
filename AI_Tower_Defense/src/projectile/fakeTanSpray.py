import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class FakeTanSpray(Projectile):
    
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 20                        # fake news does a lot of damage
        self.damageType = DamageType.fakeNews   
        self.color = (200, 100, 50)   
        self.reloadTime = 1250                  # it can be spread quickly
        self.velocity = 15                      # it travels fast


    # TODO placeholder
    def draw(self, win):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-50, 50))

        color = tuple(newColor)