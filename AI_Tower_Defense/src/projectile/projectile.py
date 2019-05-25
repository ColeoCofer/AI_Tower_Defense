import pygame
from enum import Enum
import random

class DamageType(Enum):
    lazer = 0
    fire = 1
    exploding = 2
    ice = 3
    lightning = 4
    fakeNews = 5
    melee = 6

class Projectile:
    def __init__(self):
        self.damage = 1
        self.damageType = DamageType.fakeNews
        self.color = (255, 100, 50)
        self.reloadTime = 1000
        self.velocity = 5

    def fire(self, enemy):
        for weakness in enemy.weaknesses:
            if self.damageType == weakness:
                enemy.hit(self.damage, self.damageType)
                break

    def draw(self, win, tower, enemy):
            newColor = []
            for channel in self.color:
                newColor.append(channel + random.randint(-50, 50))
            
            color = tuple(newColor)