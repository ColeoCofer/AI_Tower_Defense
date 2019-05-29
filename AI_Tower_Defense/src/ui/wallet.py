import pygame
import os

class Wallet:
    def __init__(self, position, coins):
        self.x = position[0]
        self.y = position[1]
        self.width = 32
        self.height = 32
        self.coins = coins
        self.numImages = 6
        self.images = []
        self.animationCount = 0
        self.animationSpeed = 3
        self.coinFont = pygame.font.SysFont('lucidagrandettc', 24)
        self.coinColor = (250, 241, 95)

        #Load animation images
        for i in range(self.numImages):
            image = pygame.image.load(os.path.join("../assets/other/coin/", "coin_" + str(i) + ".png"))
            self.images.append(image)

    def addCoins(self, coinsToAdd):
        self.coins += coinsToAdd

    def spendCoins(self, coinsToSpend):
        ''' Returns true if the player had enough coins and flase otherwise '''
        if coinsToSpend > self.coins:
            return False
        else:
            self.coins -= coinsToSpend
            return True

    def draw(self, win):
        self.image = self.images[self.animationCount // self.animationSpeed]
        self.animationCount += 1

        #Reset the animation count if we rendered the last image
        if self.animationCount >= (self.numImages * self.animationSpeed):
            self.animationCount = 0

        coinPosition = (self.x + self.width + 10, self.y + (self.height / 5) - 4)
        coinSurface = self.coinFont.render(str(int(self.coins)), False, self.coinColor)

        win.blit(coinSurface, coinPosition)
        win.blit(self.image, (self.x, self.y))
