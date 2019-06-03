import pygame
import random
import os
from .rangeProjectile import RangeProjectile
from .projectile import DamageType
from animations.explosion import Explosion

class Fireball(RangeProjectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 4                   # fire doesn't do a lot of damage
        self.damageType = DamageType.fire
        self.reloadTime = 10
        self.velocity = 100

        self.numImages = 8
        self.width = 30
        self.height = 30
        self.attackSound = pygame.mixer.Sound("../assets/sounds/fire.wav")
        self.attackSound.set_volume(0.15)

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/fireBall", "fireBall" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]


    def finalAnimation(self, position):
        return Explosion(position)

    # fires a projectile
    def fire(self, ticks):
        for weakness in self.targetEnemy.weaknesses:
            # skip if frozen
            if self.damageType == DamageType.ice and self.targetEnemy.frozen:
                return False
            # deal damage to enemy
            if self.damageType == weakness:
                # if not (self.trainingMode):
                #     self.attackSound.play()
                self.targetEnemy.hit(self.damage, self.damageType, ticks)
                return True

        return False
