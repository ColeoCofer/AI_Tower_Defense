import pygame
from .towerButton import TowerButton

HEIGHT_GAP_PX = 4     #Distance from top of background rect
WIDTH_GAP_PX = 40     #How "spread out" the tower buttons are from each other
IMG_SIZE = (60, 60)   #Size of tower buttons
BOTTOM_PX = 40        #Area where name and cost are displayed

class Menu:
    ''' Creates a purchase menu of tower buttons '''
    def __init__(self, position, towers):
        self.buttons = []
        self.position = position

        #Create a button for every tower
        totalSizeX = 0
        i = 0
        for i in range(len(towers)):
            if i == -1:
                #Position the first image at the front
                buttonPositionX = self.position[0] + WIDTH_GAP_PX
            else:
                #Position consecutive buttons after each other
                buttonPositionX = (i * (IMG_SIZE[0] + (WIDTH_GAP_PX))) + self.position[0]

            #Create a dummy tower object to get the data members
            tower = towers[i]((0, 0))
            resizedTowerImage = pygame.transform.scale(tower.image, IMG_SIZE)
            self.buttons.append(TowerButton((buttonPositionX, self.position[1] + HEIGHT_GAP_PX), IMG_SIZE, resizedTowerImage, tower.name, tower.cost, towers[i]))

        self.width = (len(towers) * (IMG_SIZE[0] + WIDTH_GAP_PX)) - WIDTH_GAP_PX
        self.height = IMG_SIZE[1] + HEIGHT_GAP_PX + BOTTOM_PX
        self.bgRect = pygame.Surface((self.width, self.height))
        self.bgRect.set_alpha(220)
        self.bgRect.fill((137, 139, 145))

    def draw(self, win):
        ''' Draws the tower buttons over the background rect '''

        #Draw the background
        win.blit(self.bgRect, self.position)

        #Render the buttons over the background
        for button in self.buttons:
            button.draw(win)


    def handleEvents(self, mousePosition, wallet, towerGrid):
        '''
        Handle if the user selects a tower button
        Returns the tower type if a user selected one for purchasing
        '''
        buttonWasSelected = False
        i = 0
        for i in range(len(self.buttons)):
            isSelected, towerType, towerLocation = self.buttons[i].handleEvents(mousePosition, wallet, towerGrid)

            #If they purchased one, deselect all and return the tower to place
            if isSelected == False and towerType != None:
                for button in self.buttons:
                    button.isSelected = False
                return towerType, buttonWasSelected, towerLocation

            #If we selected a new button, deselect the rest of them
            if isSelected == True:
                for j in range(len(self.buttons)):
                    if j != i:
                        #Deselect all other buttons
                        self.buttons[j].isSelected = False
                        buttonWasSelected = True
                return towerType, buttonWasSelected, towerLocation

        return towerType, buttonWasSelected, towerLocation

    def handleHoverEvents(self):
        for button in self.buttons:
            button.handleHoverEvents()
