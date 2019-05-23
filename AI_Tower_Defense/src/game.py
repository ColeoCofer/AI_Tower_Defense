import pygame
import os
import random
from enemies.zombie import Zombie

WIN_WIDTH = 1200
WIN_HEIGHT = 800


def main():
    ''' Entry point for game '''
    #Setup Game
    pygame.init()
    pygame.display.set_caption("AI Tower Defense")

    #Setup Fonts
    pygame.font.init()

    #Kick off main game loop
    g = Game()
    g.run()

'''
Setup initial window and settings.
Renders all objects and background to the screen.
Handles user events (keyboard, mouse, etc)
Keeps track of score.
'''
class Game:
    def __init__(self):
        ''' Initial window setup '''
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemies = []
        self.numEnemiesPerLevel = 10
        self.towers = []
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("../assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height)) #Scale to window (Make sure aspect ratio is the same)
        self.clicks = [] #Temp

        #Fonts
        self.uiFont = pygame.font.SysFont('lucidagrandettc', 24)



    def run(self):
        ''' Main game loop '''
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(60)
            self.spawnEnemies()
            self.handleEvents()
            self.removeEnemies()
            self.draw()

        pygame.quit()


    def handleEvents(self):
        ''' Handle keyboard and mouse events '''

        #Check for active pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #Store mouse clicks to determine path for enemies
            mousePosition = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicks.append(mousePosition)
                print(self.clicks)


    def removeEnemies(self):
        ''' Removes enemies that have walked off screen'''
        enemiesToDelete = []
        for enemy in self.enemies:
            if enemy.x > WIN_WIDTH:
                self.enemies.remove(enemy)


    def spawnEnemies(self):
        shouldSpawn = random.random()
        if shouldSpawn <= 0.1 and len(self.enemies) < self.numEnemiesPerLevel:
            randVelocity = random.randint(4, 10)
            randVerticalOffset = random.randint(-25, 25)
            self.enemies.append(Zombie(randVelocity, randVerticalOffset))


    def draw(self):
        '''
        Redraw objects onces per frame.
        Objects will be rendered sequentially,
        meaning the code at the end will be rendered above all.
        '''
        #Render the background
        self.win.blit(self.bg, (0, 0))

        #Uncomment to see clicked dots for path finding
        for p in self.clicks:
            pygame.draw.circle(self.win, (255, 0, 0), (p[0], p[1]), 5, 0)

        #Render enemies
        for enemy in self.enemies:
            enemy.draw(self.win)

        #Render UI Text Elements
        self.displayTextUI(self.win)

        #Update the window
        pygame.display.update()


    def displayTextUI(self, win):
        ''' Render UI elements above all other graphics '''

        #Enemies Remaining Surface UI
        numEnemiesText = "Enemies Remaining: " + str(len(self.enemies))
        numEnemiesPosition = (WIN_WIDTH-300, WIN_HEIGHT-50)
        numEnemiesColor = (255, 255, 255)
        numEnemiesSurface = self.uiFont.render(numEnemiesText, False, numEnemiesColor)
        win.blit(numEnemiesSurface, numEnemiesPosition)


if __name__ == "__main__":
    main()
