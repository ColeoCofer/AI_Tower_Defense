import pygame
import random
import os
from .projectile import Projectile
from .projectile import DamageType


class Punch(Projectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 5                        # punches do a lot of damage, but are kind of slow
        self.damageType = DamageType.melee
        self.color = (200, 100, 50)
        self.reloadTime = 15
        self.velocity = 5
        self.numImages = 1
        self.width = 35
        self.height = 35
        self.attackAnimationDuration = 4
