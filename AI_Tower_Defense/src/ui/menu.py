import pygame
from .towerButton import TowerButton

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Now selects tower and draws it at mouse position
HEIGHT_GAP_PX = 4     #Distance from top of background rect
WIDTH_GAP_PX = 40     #How "spread out" the tower buttons are from each other
IMG_SIZE = (60, 60)   #Size of tower buttons
BOTTOM_PX = 40        #Area where name and cost are displayed
<<<<<<< HEAD
=======
GAP_PX = 2
IMG_SIZE = (60, 60)
>>>>>>> Got the basic menu displaying
=======
GAP_PX = 1
=======
HEIGHT_GAP_PX = 4
WIDTH_GAP_PX = 40
>>>>>>> Got the menu looking much better
IMG_SIZE = (60, 60)
BOTTOM_PX = 40 #Area where name and cost is
>>>>>>> Got the name and cost displayed but it needs some tweaking
=======
>>>>>>> Now selects tower and draws it at mouse position

class Menu:
    ''' Creates a purchase menu of tower buttons '''
    def __init__(self, position, towers):
        self.buttons = []
        self.position = position

        #Create a button for every tower
        totalSizeX = 0
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
        for tower in towers:
            buttonPosition = position + GAP + lastImgX
=======
        i = 0
        for i in range(len(towers)):
<<<<<<< HEAD
<<<<<<< HEAD
            buttonPosition = position[0] + GAP_PX + lastImgX
            tower = towers[i]((0, 0))
>>>>>>> Got the basic menu displaying
=======
            # buttonPosition = position[0] + GAP_PX + lastImgX        #Add a gap between each image
            buttonPosition = i * IMG_SIZE[0] + GAP_PX + self.position[0]
            tower = towers[i]((0, 0))                               #Create a dummy tower object to get the data members
>>>>>>> Got the name and cost displayed but it needs some tweaking
=======
            if i == -1:
                #Position the first image at the front
                buttonPositionX = self.position[0] + WIDTH_GAP_PX
            else:
                #Position consecutive buttons after each other
                buttonPositionX = (i * (IMG_SIZE[0] + (WIDTH_GAP_PX))) + self.position[0]

            #Create a dummy tower object to get the data members
            tower = towers[i]((0, 0))
>>>>>>> Got the menu looking much better
            resizedTowerImage = pygame.transform.scale(tower.image, IMG_SIZE)
            self.buttons.append(TowerButton((buttonPositionX, self.position[1] + HEIGHT_GAP_PX), IMG_SIZE, resizedTowerImage, tower.name, tower.cost))

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> Save point before running
=======
        # self.width = (IMG_SIZE[0] *  + (len(towers) * GAP_PX)
=======
>>>>>>> Lots of progress with path bounds
        self.width = (len(towers) * (IMG_SIZE[0] + WIDTH_GAP_PX)) - WIDTH_GAP_PX
        self.height = IMG_SIZE[1] + HEIGHT_GAP_PX + BOTTOM_PX
        self.bgRect = pygame.Surface((self.width, self.height))
<<<<<<< HEAD
<<<<<<< HEAD
        self.bgRect.fill((234, 209, 161))
>>>>>>> Got the name and cost displayed but it needs some tweaking
=======
        self.bgRect.set_alpha(200)
=======
        self.bgRect.set_alpha(220)
>>>>>>> Added color variance in health text
        self.bgRect.fill((137, 139, 145))
>>>>>>> Got the menu looking much better

    def draw(self, win):
        ''' Draws the tower buttons over the background rect '''

        #Draw the background
        win.blit(self.bgRect, self.position)

        #Render the buttons over the background
<<<<<<< HEAD
<<<<<<< HEAD
        for button in self.buttons:
            button.draw(win)


    def handleEvents(self, mousePosition, wallet, pathBounds):
        '''
        Handle if the user selects a tower button
        Returns the tower type if a user selected one for purchasing
        '''
        buttonWasSelected = False
        i = 0
        for i in range(len(self.buttons)):
            isSelected, towerType = self.buttons[i].handleEvents(mousePosition, wallet, pathBounds)

            #If they purchased one, deselect all and return the tower to place
            if isSelected == False and towerType != None:
                for button in self.buttons:
                    button.isSelected = False
                return towerType, buttonWasSelected

            #If we selected a new button, deselect the rest of them
            if isSelected == True:
                for j in range(len(self.buttons)):
                    if j != i:
                        #Deselect all other buttons
                        self.buttons[j].isSelected = False
                        buttonWasSelected = True
                return towerType, buttonWasSelected

        return towerType, buttonWasSelected
=======
        for button in buttons:
            button.draw()
>>>>>>> Save point before running
=======
        for button in self.buttons:
            button.draw(win)
<<<<<<< HEAD
>>>>>>> Got the basic menu displaying
=======

<<<<<<< HEAD
    def handleEvents(self, mousePosition):
        for button in self.buttons:
            button.handleEvents(mousePosition)
>>>>>>> Got the name and cost displayed but it needs some tweaking
=======

    def handleEvents(self, mousePosition, wallet):
        ''' Handle if the user selects a tower button '''
        i = 0
        for i in range(len(self.buttons)):
            isSelected = self.buttons[i].handleEvents(mousePosition, wallet)

            #If we selected a new button, deselect the rest of them
            if isSelected == True:
                for j in range(len(self.buttons)):
                    if j != i:
                        #Deselect all other buttons
                        self.buttons[j].isSelected = False
                break
>>>>>>> Now selects tower and draws it at mouse position
