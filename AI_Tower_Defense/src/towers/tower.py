import pygame
from projectile.projectile import Projectile, DamageType
from animations.animation import Animation

HEALTH_GREEN = (255, 0, 0)
HEALTH_RED = (0,128,0)

class Tower:
    def __init__(self, position):
        self.position = position
        self.x = position[0]   #Position on map
        self.y = position[1]
        self.attackRadius = 0  #Distance it can attach enemies from
        self.closeEnemies = []

        self.maxHealth = 5
        self.health = self.maxHealth
        self.healthBarWidth = 50
        self.healthBarHeight = 10
        self.healthBarYOffset = 10   #Larger numbers will move the health bar closer to the enemies head
        self.weaknesses = []
        self.canAttackTime = 0 #Timestamp showing when tower can attack again
        self.attackAnimationStopTime = 0
        self.projectileColor = (255, 255, 255)

        self.projectilesFired = []
        self.animations = []

        self.image = None      #Current image being displayed
        self.width = 64        #Width of animation images
        self.height = 64       #Height of animation images


    def attack(self, enemies, win):
        '''
        Looks for enemies within it's attack radius
        Will find the closest one and attack it
        '''
        self.closeEnemies = enemies

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
                projectileToFire = self.loadProjectile(enemies[closestEnemyIndex])
                projectileToFire.enemies = enemies
                self.canAttackTime = ticks + projectileToFire.reloadTime
                projectileToFire.attackAnimationStopTime = ticks + projectileToFire.attackAnimationDuration
                projectileToFire.color = self.projectileColor
                projectileToFire.fire()
                self.projectilesFired.append(projectileToFire)                

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

        i = 0
        while i < len(self.projectilesFired):
            if self.projectilesFired[i].attackAnimationStopTime < pygame.time.get_ticks():
                del self.projectilesFired[i]
                continue
            if self.projectilesFired[i].draw(win) == True:    
                self.addAnimationToQueue(self.projectilesFired[i])
                del self.projectilesFired[i]
            i += 1

        for j in range(len(self.animations)):
            self.animations[j].draw(win)  
            if self.animations[j].attackAnimationStopTime < pygame.time.get_ticks():
                del self.animations[j]
                continue
              
        self.drawHealthBox(win, centerX, centerY)
        win.blit(self.image, (centerX, centerY))


    def hit(self, damage, damageType):
        ''' Returns true if the enemy died and subtracts damage from its health '''
        self.health = self.health - damage


    def loadProjectile(self, enemy):
        return Projectile(self.position, enemy)


    def addAnimationToQueue(self, projectile):
        animation = projectile.finalAnimation(projectile.enemyStartingPosition)
        animation.attackAnimationStopTime = pygame.time.get_ticks() + animation.attackAnimationDuration
        self.animations.append(animation)
