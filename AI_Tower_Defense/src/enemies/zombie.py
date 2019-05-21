import pygame
import os
from .enemy import Enemy

class Zombie(Enemy):
    NUM_IMAGES = 4

    #Load in the images
    images = []
    for i in range(NUM_IMAGES):
        image = pygame.image.load(os.path.join("../assets/zombie", "zombie_" + str(i) + ".gif"))
        # images.append(pygame.transform.scale(image, (64, 64)))
        images.append(image)
