import pygame

TEXT_GAP_PX = 15

class TowerButton:
    ''' A button with a picture of the tower, title, and cost '''
    def __init__(self, position, size, image, title, cost, type):
        self.type = type
        self.position = position
        self.size = size
        self.image = image
        self.title = title
        self.cost = cost
        self.rect = pygame.Rect(self.position, self.size)
        self.titleFont = pygame.font.SysFont('lucidagrandettc', 12)
        self.costFont = pygame.font.SysFont('lucidagrandettc', 15)
        self.titleColor = (0, 0, 0)
        self.costColor = (250, 241, 95)
        self.isSelected = False

    def draw(self, win):
        ''' Draw the button containing an image of the tower '''
        win.blit(self.image, self.rect)
        namePosition = (self.position[0], self.position[1] + self.size[1])
        self.displayText(self.title, namePosition, self.titleColor, win, self.titleFont)
        costPosition = (namePosition[0], namePosition[1] + TEXT_GAP_PX)
        self.displayText(str(self.cost), costPosition, self.costColor, win, self.costFont)

        self.isPlacingTower(win)

    def handleEvents(self, mousePosition, wallet, towerGrid):
        '''
        Attempts to purchase the tower if the user clicks on it
        Returns the name of the tower so we can reset all isSelected values in menu
        '''
        #Check if they clicked within bounds of the button
        if self.rect.collidepoint(mousePosition):
            #Check if they have enough coins
            if wallet.coins >= self.cost and self.isSelected == False:
                self.isSelected = True
                return True, self.type, None
        #Check if they have already selected a tower, and tried place it at a valid location
        elif self.isSelected == True and wallet.coins >= self.cost:
            towerLocation = self.canPlaceTower(towerGrid)
            if towerLocation != None:
                wallet.spendCoins(self.cost)
                self.isSelected = False
                return False, self.type, towerLocation

        return False, None, None

    def handleHoverEvents(self):
        ''' Handle if user hovers mouse over tower button '''
        #Create a transparent rectangle
        #Display enemies that are weak to each tower
        #Display info about it?
        #Create a description memeber maybe for each tower

        self.bgRect = pygame.Surface((120, 40))
        self.bgRect.set_alpha(100)
        self.bgRect.fill((137, 139, 145))




    def canPlaceTower(self, towerGrid):
        ''' Returns the location to place a tower if the current mouse position is in an empty grid space'''
        mousePosition = pygame.mouse.get_pos()
        i = 0
        for i in range(len(towerGrid)):
            #Return true if user attempts to place a tower in an empty cell
            if towerGrid[i][1] == False and towerGrid[i][0].collidepoint(mousePosition):
                towerGrid[i] = ((towerGrid[i][0], True))

                return towerGrid[i][0]
        return None


    def canPlaceTowerOutsideOfPath(self, pathBounds):
        '''
        Returns true if the current mouse position is a valid place to build a tower
        This is the old way without using the grid. It just looks if the user is trying to place it on the path or not
        '''
        mousePosition = pygame.mouse.get_pos()
        w, h = (self.size[0]/2), (self.size[1]/2) #Half the width of the tower image
        for rect in pathBounds:
            #If we collide with any of these rectangles, return False
            x, y = mousePosition[0], mousePosition[1]
            if rect.collidepoint((x-w, y-h)) or rect.collidepoint((x-w, y+h)) or rect.collidepoint((x+w, y-h)) or rect.collidepoint((x+w, y+h)):
                return False
        return True

    def isPlacingTower(self, win):
        ''' Checks if the user is currently placing a tower and draws it on the mouse position '''
        if self.isSelected == True:
            mousePosition = pygame.mouse.get_pos()
            win.blit(self.image, (mousePosition[0] - (self.size[0] / 2), mousePosition[1] - (self.size[1] / 2)))

    def displayText(self, text, position, color, win, font):
        ''' Displays the text at the given position '''
        fontSurface = font.render(text, False, color)
        win.blit(fontSurface, position)

    def drawEnemyHud(self, towerType):
        '''
        Displays information in a rectangle hud about each tower when
        the user hovers over the tower button
        '''
