import pygame
import random
from .projectile import Projectile
from .projectile import DamageType
from constants.animationConstants import PLAY_SOUND_AFFECTS

class IceBeam(Projectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 0                     # ice does no damage but freezes the oponent for other attacks
        self.damageType = DamageType.ice
        self.color = (9, 146, 208)
        self.reloadTime = 12              # is slowish to reload
        self.velocity = 5
        self.attackSound = pygame.mixer.Sound("../assets/sounds/ice.wav")
        self.attackSound.set_volume(0.1)
        self.attackAnimationDuration = 4


    # draws a simple blue line
    def draw(self, win, ticks, visualMode):
        if visualMode:    
            newColor = []
            for channel in self.color:
                newColor.append(channel + random.randint(-8, 45))
            color = tuple(newColor)
            pygame.draw.line(win, color, self.towerPosition, (self.targetEnemy.x, self.targetEnemy.y), 5)


    def fire(self, ticks):
        for weakness in self.targetEnemy.weaknesses:
            # skip if frozen
            if self.damageType == DamageType.ice and self.targetEnemy.frozen:
                return False
            # deal damage to enemy
            if self.damageType == weakness:
                if PLAY_SOUND_AFFECTS:
                    self.attackSound.play()
                self.targetEnemy.hit(self.damage, self.damageType, ticks)
                return True

        return False
