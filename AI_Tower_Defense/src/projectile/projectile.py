import pygame
from enum import Enum

class DamageType(Enum):
    lazer = 0
    fire = 1

class Projectile:
    def __init__(self):
        self.damage = 1
        self.damageType = None
        self.color = (255, 100, 50)
        self.reloadTime = 1000
        self.velocity = 5
