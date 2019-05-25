import pygame
from projectile.projectile import Projectile

HEALTH_GREEN = (255, 0, 0)
HEALTH_RED = (0,128,0)

class Tower:
    def __init__(self, position):
        self.x = position[0]   #Position on map
        self.y = position[1]
        self.attackRadius = 0  #Distance it can attach enemies from
        self.projectile = Projectile()
        self.maxHealth = 5
        self.health = self.maxHealth
        self.healthBarWidth = 50
        self.healthBarHeight = 10
        self.healthBarYOffset = 10   #Larger numbers will move the health bar closer to the enemies head
        self.weaknesses = []
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

            # TODO this is where we would need to be selective about what we add to the attack queue
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

    def drawHealthBox(self, win, centerX, centerY):
        ''' Draws a health box above each tower '''
        if self.health > 0:
            healthBarX = self.x - (self.healthBarWidth / 2)
            healthBarY = self.y - self.height + self.healthBarYOffset
            if self.health == self.maxHealth:
                pygame.draw.rect(win, HEALTH_GREEN, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Outline of health bar
                pygame.draw.rect(win, HEALTH_RED, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Inside of health bar
            else:
                pygame.draw.rect(win, HEALTH_GREEN, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Outline health bar
                pygame.draw.rect(win, HEALTH_RED, (healthBarX, healthBarY, (self.healthBarWidth / self.maxHealth) * self.health, self.healthBarHeight))


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

        self.drawHealthBox(win, centerX, centerY)

        win.blit(self.image, (centerX, centerY))

    def hit(self, damage):
        ''' Returns true if the enemy died and subtracts damage from its health '''
        self.health = self.health - damage
