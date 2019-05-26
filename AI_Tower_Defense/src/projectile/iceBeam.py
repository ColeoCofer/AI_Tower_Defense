import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class IceBeam(Projectile):
    
    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 0                     # ice does no damage but freezes the oponent for other attacks
        self.damageType = DamageType.ice
        self.color = (9, 146, 208)
        self.reloadTime = 1250              # is slowish to reload
        self.velocity = 5


    # draws a simple blue line
    def draw(self, win):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-8, 45))
        color = tuple(newColor)
        pygame.draw.line(win, color, self.towerPosition, (self.targetEnemy.x, self.targetEnemy.y), 5)