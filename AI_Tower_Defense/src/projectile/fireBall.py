import pygame
import random
from .projectile import Projectile
from .projectile import DamageType


class Fireball(Projectile):

    def __init__(self, towerPosition, enemy, enemies):
        super().__init__(towerPosition, enemy, enemies)
        self.damage = 5                     # fire doesn't do a lot of damage
        self.damageType = DamageType.fire
        self.color = (200, 100, 50)
        self.reloadTime = 750
        self.velocity = 5
        self.numImages = 8

    # TODO placeholder
    def draw(self, win):
        newColor = []
        for channel in self.color:
            newColor.append(channel + random.randint(-50, 50))

        color = tuple(newColor)

        #Load images
        for i in range(0, self.numImages):
            image = pygame.image.load(os.path.join("../assets/projectiles/fireBall", "fireBall" + str(i) + ".png"))
            self.images.append(pygame.transform.scale(image, (self.width, self.height)))
        self.image = self.images[0]

        # need to add how projectiles are rendered
