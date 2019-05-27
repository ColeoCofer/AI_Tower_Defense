import pygame

class TowerButton:
    ''' A button with a picture of the tower, title, and cost '''
    def __init__(self, position, size, image, title, cost):
        self.position = position
        self.size = self.size
        self.image = image
        self.title = title
        self.cost = cost
        self.rect = pygame.Rect(self.position, self.size)

    def draw(self):
        ''' Draw the button containing an image of the tower '''
        screen.blit(self.image, self.rect)

    def didClick(self, event):
        ''' Attempts to purchase the tower if the user clicks on it '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print(f"You clicked the {self.title} button!")
                #This is where we'd attempt to but the tower
