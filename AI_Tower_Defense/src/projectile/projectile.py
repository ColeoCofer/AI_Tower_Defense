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
    def __init__(self, towerPosition, enemy):
        self.towerPosition = towerPosition
        self.enemyStartingPosition = (enemy.x, enemy.y)
        self.targetEnemy = enemy
        self.x = towerPosition[0]
        self.y = towerPosition[1]

        self.damage = 1
        self.damageType = None
        self.color = (255, 100, 50)
        self.reloadTime = 1000
        self.velocity = 5
        self.images = []
        self.image = None
        
        self.animationSpeed = 3
        self.animationCount = 0
        
        self.attackAnimationStopTime = 0
        self.attackAnimationDuration = 200


    def fire(self):
        for weakness in self.targetEnemy.weaknesses:
            if self.damageType == DamageType.ice and self.targetEnemy.frozen:
                    continue
            if self.damageType == weakness:
                self.targetEnemy.hit(self.damage, self.damageType)
                

    def draw(self, win):
        return
