import os
import pygame
import random
import math
from .projectile import DamageType
from .rangeProjectile import RangeProjectile
from animations.fireExplosion import FireExplosion
from constants.animationConstants import PLAY_SOUND_AFFECTS


class Cannonball(RangeProjectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 8                         # cannonballs also do half this damage to the surroundings
        self.damageType = DamageType.exploding  # cannonballs go boom
        self.reloadTime = 30                    # reload time long
        self.velocity = 100                     # cannonballs are fast


        self.numImages = 5
        self.width = 30
        self.height = 30
        self.attackSound = pygame.mixer.Sound("../assets/sounds/cannonShot.flac")
        self.attackSound.set_volume(0.15)

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/cannonball", "cannonball" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]


    # calulates the addtional surrounding damage
    def explosiveDamage(self, ticks):
        for enemy in self.enemies:
            dist = (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2
            #Use radius squared to avoid taking square roots of distance
            if dist <= self.attackRadius ** 2:
                # if not self.trainingMode:
                #     self.attackSound.play()
                halfDamage = self.damage / 2
                enemy.hit(halfDamage, self.damageType, ticks)
                self.damage += halfDamage
                if PLAY_SOUND_AFFECTS:
                    self.attackSound.play()


    # returns a residual animation
    def finalAnimation(self, position):
        return FireExplosion(position)
