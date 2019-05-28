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
