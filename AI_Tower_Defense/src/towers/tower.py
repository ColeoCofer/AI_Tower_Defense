import pygame
from projectile.lazer import Lazer

class Tower:
    def __init__(self, position):
        self.x = position[0]   #Position on map
        self.y = position[1]
        self.attackRadius = 0  #Distance it can attach enemies from
        self.projectile = Lazer()

        #self.damage = 0        #Amount of damage delt per attack
        #self.coolDown = 1000   #Time between attacks in ms

        self.canAttackTime = 0 #Timestamp showing when tower can attack again
        self.attackAnimationDuration = 200
        self.attackAnimationTimeStamp = 0
        self.enemiesBeingAttacked = []
        self.image = None      #Current image being displayed
        self.width = 64        #Width of animation images
        self.height = 64       #Height of animation images


    def attack(self, enemies, win):
        '''
        Looks for enemies within it's attack radius
        Will find the closest one and attack it
        '''
        #Check if the tower is ready to attack again
        ticks = pygame.time.get_ticks()
        if ticks >= self.canAttackTime:
            attackableEnemies = []
            i = 0
            for enemy in enemies:
                dist = (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2
                #Use radius squared to avoid taking square roots of distance
                if dist <= self.attackRadius ** 2:
                    attackableEnemies.append((i, dist))
                i += 1

            if len(attackableEnemies) > 0:
                closestEnemyIndex = (min(attackableEnemies, key = lambda enemy: enemy[1]))[0]
                self.attackAnimationTimeStamp = ticks + self.attackAnimationDuration

                enemyX, enemyY = enemies[closestEnemyIndex].x, enemies[closestEnemyIndex].y
                self.enemiesBeingAttacked.append((enemyX, enemyY))
                self.projectile.fire(enemies[closestEnemyIndex])
                self.canAttackTime = ticks + self.projectile.reloadTime

        return enemies


    def draw(self, win):
        ''' Render the tower to the map '''
        centerX = self.x - (self.width / 2)
        centerY = self.y - (self.height / 2)

        #Check if we should display the attack animation
        if pygame.time.get_ticks() <= self.attackAnimationTimeStamp:
            for enemy in self.enemiesBeingAttacked:
                self.projectile.draw(win, (self.x, self.y), enemy)
        else:
            self.enemiesBeingAttacked = []

        win.blit(self.image, (centerX, centerY))
