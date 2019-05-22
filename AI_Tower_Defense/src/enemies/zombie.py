import pygame
import os
from .enemy import Enemy

class Zombie(Enemy):
    numImages = 4

    def __init__(self):
        super().__init__() #I'm not sure if this is necessary...
        self.images = []
        for i in range(self.numImages):
            image = pygame.image.load(os.path.join("../assets/zombie", "zombie_" + str(i) + ".png"))
            #Uncomment to transform to different size
            #images.append(pygame.transform.scale(image, (64, 64)))
            self.images.append(image)
