import pygame
from .projectile import Projectile
from .projectile import DamageType

class Lazer(Projectile):
    def __init__(self):
        super().__init__()
        self.damage = 1
        self.damageType = DamageType.lazer
        self.color = (255, 100, 50)
        self.reloadTime = 1000
        self.velocity = 5

    def draw(self, win, tower, enemy):
        pygame.draw.line(win, self.color, tower, enemy, 5)


    def fire(self, enemy):
        #TODO: Check for weaknesses
        enemy.hit(self.damage)
