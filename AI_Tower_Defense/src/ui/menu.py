import pygame
from .towerButton import TowerButton

GAP_PX = 1
IMG_SIZE = (60, 60)
BOTTOM_PX = 40 #Area where name and cost is

class Menu:
    ''' Creates a purchase menu of tower buttons '''
    def __init__(self, position, towers):
        self.buttons = []
        self.position = position
        self.font = pygame.font.SysFont('lucidagrandettc', 18)
        self.fontColor = (250, 241, 95)

        #Create a button for every tower
        totalSizeX = 0
        i = 0
        for i in range(len(towers)):
            # buttonPosition = position[0] + GAP_PX + lastImgX        #Add a gap between each image
            buttonPosition = i * IMG_SIZE[0] + GAP_PX + self.position[0]
            tower = towers[i]((0, 0))                               #Create a dummy tower object to get the data members
            resizedTowerImage = pygame.transform.scale(tower.image, IMG_SIZE)
            self.buttons.append(TowerButton((buttonPosition, self.position[1] + GAP_PX), IMG_SIZE, resizedTowerImage, tower.name, tower.cost))

        # self.width = (IMG_SIZE[0] *  + (len(towers) * GAP_PX)
        self.width = len(towers) * (IMG_SIZE[0] + GAP_PX)
        self.height = IMG_SIZE[1] + GAP_PX * 2 + BOTTOM_PX
        self.bgRect = pygame.Surface((self.width, self.height))
        self.bgRect.fill((234, 209, 161))

    def draw(self, win):
        ''' Draws the tower buttons over the background rect '''

        #Draw the background
        win.blit(self.bgRect, self.position)

        #Render the buttons over the background
        for button in self.buttons:
            button.draw(win)

    def handleEvents(self, mousePosition):
        for button in self.buttons:
            button.handleEvents(mousePosition)
