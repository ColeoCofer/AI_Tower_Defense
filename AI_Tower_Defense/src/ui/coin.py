import pygame

class Coin:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.coins = 0
        self.numImages = 6
        self.images = []
        self.animationCount = 0
        self.animationSpeed = 3

        #Load animation images
        for i in range(self.numImages):
            image = pygame.image.load(os.path.join("../assets/ui/other/", "coin_" + str(i) + ".png"))
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

    def draw(self):
        self.image = self.images[self.animationCount // self.animationSpeed]
        self.animationCount += 1

        #Reset the animation count if we rendered the last image
        if self.animationCount >= (numImages * self.animationSpeed):
            self.animationCount = 0

    win.blit(self.image, (self.x, self.y))
