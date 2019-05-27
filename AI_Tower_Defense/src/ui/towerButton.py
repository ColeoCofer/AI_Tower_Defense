import pygame

TEXT_GAP_PX = 15

class TowerButton:
    ''' A button with a picture of the tower, title, and cost '''
    def __init__(self, position, size, image, title, cost):
        self.position = position
        self.size = size
        self.image = image
        self.title = title
        self.cost = cost
        self.rect = pygame.Rect(self.position, self.size)
        self.font = pygame.font.SysFont('lucidagrandettc', 10)
        self.titleColor = (0, 0, 0)
        self.costColor = (160, 141, 95)

    def draw(self, win):
        ''' Draw the button containing an image of the tower '''
        win.blit(self.image, self.rect)
        namePosition = (self.position[0], self.position[1] + self.size[1])
        self.displayText(self.title, namePosition, self.titleColor, win)
        costPosition = (namePosition[0], namePosition[1] + TEXT_GAP_PX)
        self.displayText(str(self.cost), costPosition, self.costColor, win)

    def handleEvents(self, mousePosition):
        ''' Attempts to purchase the tower if the user clicks on it '''
        if self.rect.collidepoint(mousePosition):
            print(f"You clicked the {self.title} button!")
            #This is where we'd attempt to but the tower

    def displayText(self, text, position, color, win):
        ''' Displays the text at the given position '''
        fontSurface = self.font.render(text, False, color)
        win.blit(fontSurface, position)
