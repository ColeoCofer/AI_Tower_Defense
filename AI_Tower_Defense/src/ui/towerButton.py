import pygame
from enemies.zombie import Zombie
from constants.gameConstants import *

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
        self.shouldDrawEnemyHud = False
        self.playedHoverSound = False
        self.hoverClickSound =  pygame.mixer.Sound("../assets/sounds/clickTower.ogg")
        self.hoverClickSound.set_volume(0.4)
        self.selectTowerSound = pygame.mixer.Sound("../assets/sounds/selectTower.ogg")
        self.selectTowerSound.set_volume(0.8)
        self.placedTowerSound = pygame.mixer.Sound("../assets/sounds/placeTower.ogg")
        self.placedTowerSound.set_volume(1)


    def draw(self, win):
        ''' Draw the button containing an image of the tower '''
        win.blit(self.image, self.rect)
        namePosition = (self.position[0], self.position[1] + self.size[1])
        self.displayText(self.title, namePosition, self.titleColor, win, self.titleFont)
        costPosition = (namePosition[0], namePosition[1] + TEXT_GAP_PX)
        self.displayText(str(self.cost), costPosition, self.costColor, win, self.costFont)
        self.isPlacingTower(win)

        if self.shouldDrawEnemyHud:
            self.drawEnemyHud(win)

    def handleEvents(self, mousePosition, wallet, towerGrid):
        '''
        Attempts to purchase the tower if the user clicks on it
        Returns the name of the tower so we can reset all isSelected values in menu
        '''
        #Check if they clicked within bounds of the button
        if self.rect.collidepoint(mousePosition):
            #Check if they have enough coins
            if wallet.coins >= self.cost and self.isSelected == False:
                self.selectTowerSound.play()
                self.isSelected = True
                return True, self.type, None
        #Check if they have already selected a tower, and tried place it at a valid location
        elif self.isSelected == True and wallet.coins >= self.cost:
            towerLocation = self.canPlaceTower(towerGrid)
            if towerLocation != None:
                self.placedTowerSound.play()
                self.isSelected = False
                return False, self.type, towerLocation

        return False, None, None

    def drawEnemyHud(self, win):
        '''
        Displays information in a rectangle hud about each tower when
        the user hovers over the tower button
        '''

        # Transparent rectangle for the background
        self.bgRect = pygame.Surface((355, 120))
        self.bgRect.set_alpha(100)
        self.bgRect.fill((137, 139, 145))
        bgRectPos = (self.position[0], self.position[1] - 140)

        tower = self.type((0, 0))
        projectileType = tower.loadProjectile(Zombie(0))
        damageType = projectileType.damageType.name
        damageAmt = projectileType.damage
        weaknesses = tower.weaknesses
        attackRadius = round(tower.attackRadius / TOWER_GRID_SIZE, 1)

        weaknessString = "Weaknesses: "
        for weakness in weaknesses:
            weaknessString += weakness.name + ", "
        weaknessString = weaknessString[:-2] #Get rid of last comma

        damageString = "Damage Type: " + damageType
        damageAmtString = "Damage: " + str(damageAmt)
        attackRadiusString = "Attack Radius: " + str(attackRadius) + " Grids"


        win.blit(self.bgRect, bgRectPos)

        self.displayText(weaknessString, (bgRectPos[0] + 10, bgRectPos[1] + 10), (255, 255, 255), win, self.costFont)
        self.displayText(damageString, (bgRectPos[0] + 10, bgRectPos[1] + 35), (255, 255, 255), win, self.costFont)
        self.displayText(damageAmtString, (bgRectPos[0] + 10, bgRectPos[1] + 60), (255, 255, 255), win, self.costFont)
        self.displayText(attackRadiusString, (bgRectPos[0] + 10, bgRectPos[1] + 85), (255, 255, 255), win, self.costFont)



    def handleHoverEvents(self):
        ''' Handle if user hovers mouse over tower button and display enemy info if so '''
        mousePosition = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePosition):
            self.shouldDrawEnemyHud = True

            if self.playedHoverSound == False:
                self.hoverClickSound.play()
                self.playedHoverSound = True

        else:
            self.shouldDrawEnemyHud = False
            self.playedHoverSound = False



    def canPlaceTower(self, towerGrid):
        ''' Returns the location to place a tower if the current mouse position is in an empty grid space'''
        mousePosition = pygame.mouse.get_pos()
        i = 0
        for i in range(len(towerGrid)):
            #Return true if user attempts to place a tower in an empty cell
            if towerGrid[i][1] == False and towerGrid[i][0].collidepoint(mousePosition):
                towerGrid[i] = ((towerGrid[i][0], True, TOWER_TYPES.index(self.type) + 1))

                return towerGrid[i][0]
        return None


    def canPlaceTowerOutsideOfPath(self, pathBounds):
        '''
        Returns true if the current mouse position is a valid place to build a tower
        This is the old way without using the grid. It just looks if the user is trying to place it on the path or not
        '''
        mousePosition = pygame.mouse.get_pos()
        w, h = (self.size[0]/2), (self.size[1]/2) #Half the width of the tower image
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
