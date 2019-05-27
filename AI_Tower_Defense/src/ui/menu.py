import pygame
from .towerButton import TowerButton

GAP_PX = 2
IMG_SIZE = (60, 60)

class Menu:
    ''' Creates a purchase menu of tower buttons '''
    def __init__(self, position, towers):
        self.buttons = []
        self.position = position

        #Create a button for every tower
        lastImgX = 0
        totalSizeX = 0
        i = 0
        for i in range(len(towers)):
            buttonPosition = position[0] + GAP_PX + lastImgX
            tower = towers[i]((0, 0))
            resizedTowerImage = pygame.transform.scale(tower.image, IMG_SIZE)
            self.buttons.append(TowerButton((buttonPosition, self.position[1]), IMG_SIZE, resizedTowerImage, tower.name, tower.cost))
            lastImgX = buttonPosition
            totalSizeX += buttonPosition

        self.width = totalSizeX
        self.height = IMG_SIZE[1] + GAP_PX
        # self.bgRect = pygame.Rect(position, (self.width, self.width))
        self.bgRect = pygame.Surface((self.width, self.width))
        self.bgRect.fill((0, 0, 0))


    def draw(self, win):
        ''' Draws the tower buttons over the background rect '''

        #Draw the background
        win.blit(self.bgRect, self.position)

        #Render the buttons over the background
        for button in self.buttons:
            button.draw(win)
