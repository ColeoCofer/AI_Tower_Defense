import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.punch import Punch
from .enemy import Enemy
from .attackingEnemy import AttackingEnemy


class Warrior(AttackingEnemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)  
        self.maxHealth = 16                             # warriors are pretty tough
        self.health = self.maxHealth
        self.velocity = random.randint(7,10)            # warriors are pretty fast
        self.weaknesses.append(DamageType.fire)
        self.weaknesses.append(DamageType.lightning)
        self.weaknesses.append(DamageType.lazer)        # warriors are weak to everything
        self.superWeakness = DamageType.fire            # and super weak to fire

        self.width = 54
        self.height = 54
        self.numImages = 20
        self.images = []
        self.animationSpeed = 2

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/warrior", "3_enemies_1_walk_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))


    # overrides base class version
    def loadProjectile(self, enemy):
        return Punch((self.x, self.y), enemy, self.closeEnemies)
