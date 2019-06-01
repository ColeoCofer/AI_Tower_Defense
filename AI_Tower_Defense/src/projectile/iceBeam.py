import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class IceBeam(Projectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 0                     # ice does no damage but freezes the oponent for other attacks
        self.damageType = DamageType.ice
        self.color = (9, 146, 208)
        self.reloadTime = 1250              # is slowish to reload
        self.velocity = 5
        self.attackSound = pygame.mixer.Sound("../assets/sounds/ice.wav")
        self.attackSound.set_volume(0.1)


    # draws a simple blue line
    def draw(self, win):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-8, 45))
        color = tuple(newColor)
        pygame.draw.line(win, color, self.towerPosition, (self.targetEnemy.x, self.targetEnemy.y), 5)

    def fire(self):
        for weakness in self.targetEnemy.weaknesses:
            # skip if frozen
            if self.damageType == DamageType.ice and self.targetEnemy.frozen:
                return False
            # deal damage to enemy
            if self.damageType == weakness:
                self.attackSound.play()
                self.targetEnemy.hit(self.damage, self.damageType)
                return True

        return False
