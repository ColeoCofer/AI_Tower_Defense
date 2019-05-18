import pygame
import os

class Game:
    def __init__(self):
        ''' Initial window setup '''
        self.width = 1000
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.towers = []
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("assets", "bg.png"))

    def run():
        ''' Main game loop '''
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)  #60 FPS
            for even in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = false

                self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        pygame.display.update()
