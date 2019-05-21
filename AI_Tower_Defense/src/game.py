import pygame
import os
from enemies.zombie import Zombie

class Game:
    def __init__(self):
        ''' Initial window setup '''
        self.width = 1200
        self.height = 800
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemies = [Zombie()]
        self.towers = []
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("../assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height)) #Scale to window (Make sure aspect ratio is the same)
        self.clicks = [] #Temp

    def run(self):
        ''' Main game loop '''

        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(30) #FPS
            pygame.time.delay(100)    ''' TEMP Make distance travelled smaller steps '''
            ''' Loop through key events '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                mousePosition = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(mousePosition)
                    print(self.clicks) #29.23 to remove clicks

                enemiesToDelete = []
                for enemy in self.enemies:
                    if enemy.x < 0:
                        enemiesToDelete.append(enemy)

                for toDelete in enemiesToDelete:
                    self.enemies.remove(toDelete)


                self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))   #Draw the background onto the screen

        #Uncomment to see click dots for path finding
        #for p in self.clicks:
        #    pygame.draw.circle(self.win, (255, 0, 0), (p[0], p[1]), 5, 0)

        for enemy in self.enemies:
            enemy.draw(self.win)

        pygame.display.update()

pygame.init()
pygame.display.set_caption("AI Tower Defense")
g = Game()
g.run()
