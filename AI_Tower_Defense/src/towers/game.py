import pygame
import os

#Left off at 26:30 but iamge is not rendering...

class Game:
    def __init__(self):
        ''' Initial window setup '''
        self.width = 1000
        self.height = 800
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.towers = []
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("../../assets", "bg.jpeg"))
        self.bt = pygame.transform.scale(self.bg, (self.width, self.height))
        self.clicks = [] #Temp

    def run(self):
        ''' Main game loop '''
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)  #60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                mousePosition = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(mousePosition)
                    print(mousePosition)

                self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))

        for p in self.clicks:
            pygame.draw.circle(self.win, (255, 0, 0), (p[0], p[1]), 5, 0)

        pygame.display.update()

g = Game()
g.run()
