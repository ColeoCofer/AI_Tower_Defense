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
<<<<<<< HEAD
<<<<<<< HEAD
        self.titleFont = pygame.font.SysFont('lucidagrandettc', 12)
        self.costFont = pygame.font.SysFont('lucidagrandettc', 15)
        self.titleColor = (0, 0, 0)
        self.costColor = (250, 241, 95)
        self.isSelected = False
<<<<<<< HEAD
=======
        self.font = pygame.font.SysFont('lucidagrandettc', 10)
        self.titleColor = (0, 0, 0)
        self.costColor = (160, 141, 95)
>>>>>>> Got the name and cost displayed but it needs some tweaking
=======
        self.titleFont = pygame.font.SysFont('lucidagrandettc', 12)
        self.costFont = pygame.font.SysFont('lucidagrandettc', 15)
        self.titleColor = (0, 0, 0)
        self.costColor = (250, 241, 95)
>>>>>>> Got the menu looking much better
=======
>>>>>>> Now selects tower and draws it at mouse position

    def draw(self, win):
        ''' Draw the button containing an image of the tower '''
        win.blit(self.image, self.rect)
<<<<<<< HEAD
<<<<<<< HEAD
        namePosition = (self.position[0], self.position[1] + self.size[1])
        self.displayText(self.title, namePosition, self.titleColor, win, self.titleFont)
        costPosition = (namePosition[0], namePosition[1] + TEXT_GAP_PX)
        self.displayText(str(self.cost), costPosition, self.costColor, win, self.costFont)

        self.isPlacingTower(win)

    def handleEvents(self, mousePosition, wallet, pathBounds):
        '''
        Attempts to purchase the tower if the user clicks on it
        Returns the name of the tower so we can reset all isSelected values in menu
        '''
        #Check if they clicked within bounds of the button
        if self.rect.collidepoint(mousePosition):
            #Check if they have enough coins
            if wallet.coins >= self.cost and self.isSelected == False:
                self.isSelected = True
                return True, None
        #Check if they have already selected a tower, and tried place it at a valid location
        elif self.isSelected == True and wallet.coins >= self.cost and self.canPlaceTower(pathBounds) == True:
            wallet.spendCoins(self.cost)
            #May need to return a tower to be created here...
            self.isSelected = False
            return False, self.type

        return False, None

    def canPlaceTower(self, pathBounds):
        ''' Returns true if the current mouse position is a valid place to build a tower '''
        mousePosition = pygame.mouse.get_pos()
        w, h = (self.size[0]/2), (self.size[1]/2)
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
=======
=======
        namePosition = (self.position[0], self.position[1] + self.size[1])
        self.displayText(self.title, namePosition, self.titleColor, win, self.titleFont)
        costPosition = (namePosition[0], namePosition[1] + TEXT_GAP_PX)
<<<<<<< HEAD
        self.displayText(str(self.cost), costPosition, self.costColor, win)
>>>>>>> Got the name and cost displayed but it needs some tweaking
=======
        self.displayText(str(self.cost), costPosition, self.costColor, win, self.costFont)
>>>>>>> Got the menu looking much better

<<<<<<< HEAD
    def handleEvents(self, mousePosition):
        ''' Attempts to purchase the tower if the user clicks on it '''
<<<<<<< HEAD
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print(f"You clicked the {self.title} button!")
                #This is where we'd attempt to but the tower
>>>>>>> Got the basic menu displaying
=======
=======
        self.isPlacingTower(win)

    def handleEvents(self, mousePosition, wallet, pathBounds):
        '''
        Attempts to purchase the tower if the user clicks on it
        Returns the name of the tower so we can reset all isSelected values in menu
        '''
        #Check if they clicked within bounds of the button
>>>>>>> Now selects tower and draws it at mouse position
        if self.rect.collidepoint(mousePosition):
            #Check if they have enough coins
            if wallet.coins >= self.cost and self.isSelected == False:
                self.isSelected = True
                return True
        elif self.isSelected == True and wallet.coints >= self.cost and canPlaceTower(pathBounds) == True:
            #Make the purchase
            #Place the tower
            self.isSelected = False

        return False

    def canPlaceTower(self, pathBounds):
        ''' Returns true if the current mouse position is a valid place to build a tower '''
        mousePosition = pygame.mouse.get_pos()


        pass

    def isPlacingTower(self, win):
        ''' Checks if the user is currently placing a tower and draws it on the mouse position '''
        if self.isSelected == True:
            mousePosition = pygame.mouse.get_pos()
            win.blit(self.image, (mousePosition[0] - (self.size[0] / 2), mousePosition[1] - (self.size[1] / 2)))

    def displayText(self, text, position, color, win, font):
        ''' Displays the text at the given position '''
        fontSurface = font.render(text, False, color)
        win.blit(fontSurface, position)
>>>>>>> Got the name and cost displayed but it needs some tweaking
