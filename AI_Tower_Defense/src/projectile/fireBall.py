import pygame
import random
import os
from .rangeProjectile import RangeProjectile
from .projectile import DamageType
from animations.explosion import Explosion

class Fireball(RangeProjectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 2                   # fire doesn't do a lot of damage
        self.damageType = DamageType.fire
        self.reloadTime = 1500
        self.velocity = 100
        self.attackRadius = 40
        self.detonationRange = 30
        self.numImages = 8
        self.width = 30
        self.height = 30
        self.attackAnimationDuration = 5000
        self.attackSound = pygame.mixer.Sound("../assets/sounds/fire.wav")
        self.attackSound.set_volume(0.15)

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/fireBall", "fireBall" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]


    def finalAnimation(self, position):
<<<<<<< HEAD
        return Explosion(position)
=======
        return FireExplosion(position)
>>>>>>> 3763082b962a5a2c5af4c44e701e1bf8a9064b11

    # fires a projectile
    def fire(self):
        for weakness in self.targetEnemy.weaknesses:
            # skip if frozen
            if self.damageType == DamageType.ice and self.targetEnemy.frozen:
                continue
            # deal damage to enemy
            if self.damageType == weakness:
                self.attackSound.play()
                self.targetEnemy.hit(self.damage, self.damageType)
