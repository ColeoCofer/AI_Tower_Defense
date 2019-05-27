import pygame
from .towerButton import TowerButton

GAP_PX = 10
IMG_SIZE = (60, 60)

class Menu:
    ''' Creates a purchase menu of tower buttons '''
    def __init__(self, position, towers):
        self.buttons = []
        self.x = position[0]
        self.y = position[1]

        #Create a button for every tower
        lastImgX = 0
        totalSizeX = 0
        for tower in towers:
            buttonPosition = position + GAP + lastImgX
            self.buttons.append(Tower(buttonPosition, IMG_SIZE, tower.image, tower.name, tower.cost))
            lastImgX = buttonPosition
            totalSizeX += buttonPosition

        self.width = totalSizeX
        self.height = IMG_SIZE[1] + GAP_PX

        self.bgRect = pygame.Rect(position, size)
