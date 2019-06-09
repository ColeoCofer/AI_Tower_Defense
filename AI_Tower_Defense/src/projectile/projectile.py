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
    poison = 7


# base class for all porjectiles
class Projectile:
    def __init__(self, towerPosition, enemy, enemies):
        self.towerPosition = towerPosition
        self.enemyStartingPosition = (enemy.x, enemy.y)
        self.targetEnemy = enemy
        self.enemies = enemies
        self.x = towerPosition[0]
        self.y = towerPosition[1]

        self.damage = 1
        self.damageType = None
        self.color = (100, 100, 100)
        self.reloadTime = 10
        self.velocity = 0

        self.images = []
        self.image = None
        self.width = 30
        self.height = 30
        self.animationSpeed = 3
        self.animationCount = 0
        self.attackAnimationStopTime = 0
        self.attackAnimationDuration = 2


    # fires a projectile
    def fire(self, ticks):
        for weakness in self.targetEnemy.weaknesses:
            # skip if frozen
            if self.damageType == DamageType.ice and self.targetEnemy.frozen:
                return False
            # deal damage to enemy
            if self.damageType == weakness:
                self.targetEnemy.hit(self.damage, self.damageType, ticks)
                return True

        return False


    # draw base class stub
    def draw(self, win, ticks, visualMode):
        return
