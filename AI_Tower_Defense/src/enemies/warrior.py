import os
import random
import pygame
from projectile.projectile import DamageType
from projectile.punch import Punch
from .attackingEnemy import AttackingEnemy
from .enemy import Enemy

class Warrior(AttackingEnemy):

    def __init__(self, yOffset):
        super().__init__(yOffset)
        self.width = 54
        self.height = 54
        self.maxHealth = 10
        self.health = self.maxHealth
        
        self.numImages = 20
        self.images = []
        self.velocity = random.randint(self.health, self.health + (self.health // 2))
        self.animationSpeed = 2
        self.weaknesses = [DamageType.fire]
        # self.projectile.color = (70, 70, 200)


        #Load images
        for i in range(1, self.numImages):
            image = pygame.image.load(os.path.join("../assets/enemy/warrior", "3_enemies_1_walk_" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))

    def loadProjectile(self, enemy):
        return Punch((self.x, self.y), enemy, self.closeEnemies)
