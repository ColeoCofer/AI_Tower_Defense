import pygame
from projectile.projectile import Projectile, DamageType
from animations.animation import Animation
from constants.animationConstants import *
from projectile.iceBeam import IceBeam
# from .igloo import Igloo


# Tower base class
class Tower:

    def __init__(self, position):
        self.name = "No Name"
        self.cost = 200
        self.position = position
        self.x = position[0]   # Position on map
        self.y = position[1]
        self.attackRadius = 192  # Distance it can attack enemies from, two grid squares
        self.closeEnemies = []
        self.startingHealth = 5
        self.health = self.startingHealth
        self.weaknesses = [DamageType.melee, DamageType.fakeNews]    # All towers are weak to the punches
        self.attackCooldownTime = 0             # Timestamp showing when tower can attack again
        self.damageDealt = 0

        self.healthBarWidth = 50
        self.healthBarHeight = 10
        self.healthBarYOffset = 10          # Larger numbers will move the health bar closer to the enemies head
        self.attackAnimationStopTime = 0
        self.projectileColor = (155, 155, 155)
        self.width = 64        # Width of animation images
        self.height = 64       # Height of animation images
        self.image = None      # Current image being displayed

        self.projectilesFired = []   # projectile magazine
        self.animations = []         # animations to render

        # for the GAs
        self.indexForRecordTable = 0

        # for deep learning
        self.damageDealtOnTurn = 0
        self.damageTakenOnTurn = 0

    # launches a tower attacking round
    def attack(self, enemies, ticks):
        '''
        Looks for enemies within it's attack radius
        Will find the closest one and attack it
        '''
        self.closeEnemies = enemies

        #Check if the tower is ready to attack again
        # ticks = pygame.time.get_ticks()

        if ticks >= self.attackCooldownTime:
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
                # taget the closest enemy and load projectile into the magazine
                closestEnemyIndex = (min(attackableEnemies, key = lambda enemy: enemy[1]))[0]
                projectileToFire = self.loadProjectile(enemies[closestEnemyIndex])
                projectileToFire.enemies = enemies
                self.attackCooldownTime = ticks + projectileToFire.reloadTime
                targetAcquired = projectileToFire.fire(ticks)
                if targetAcquired:
                    projectileToFire.attackAnimationStopTime = ticks + projectileToFire.attackAnimationDuration
                    projectileToFire.color = self.projectileColor
                    self.projectilesFired.append(projectileToFire)


        return enemies


    ''' Draws a health box above each tower '''
    def drawHealthBox(self, win, centerX, centerY):
        if self.health > 0:
            healthBarX = self.x - (self.healthBarWidth / 2)
            healthBarY = self.y - self.height + self.healthBarYOffset
            if self.health == self.startingHealth:
                pygame.draw.rect(win, HEALTH_GREEN, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Outline of health bar
                pygame.draw.rect(win, HEALTH_RED, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Inside of health bar
            else:
                pygame.draw.rect(win, HEALTH_GREEN, (healthBarX, healthBarY, self.healthBarWidth, self.healthBarHeight)) #Outline health bar
                pygame.draw.rect(win, HEALTH_RED, (healthBarX, healthBarY, (self.healthBarWidth / self.startingHealth) * self.health, self.healthBarHeight))


    # draw the tower and any of its projectiles/animations
    def draw(self, win, ticks, visualMode):

        i = 0
        # cycle through the prpjectiles in our magazine
        while i < len(self.projectilesFired):
            # check and make sure animation time hasn't lapsed
            if self.projectilesFired[i].attackAnimationStopTime < ticks:
                del self.projectilesFired[i]
                continue
            # TODO I think we may want to think about this. It currently is saying that a projectile has hit it's target
            if self.projectilesFired[i].draw(win, ticks, visualMode) == True:
                initialDamage = self.projectilesFired[i].damage
                self.damageDealt += initialDamage
                
                # deep Q 
                self.damageDealtOnTurn += initialDamage
                if type(self.projectilesFired[i]) == IceBeam:
                    self.damageDealtOnTurn += 2
                
                if visualMode:
                    # replace the projectile with its final animation in the same postion
                    self.addAnimationToQueue(self.projectilesFired[i], ticks)
                
                del self.projectilesFired[i]
            i += 1

        if visualMode:
            ''' Render the tower to the map '''
            centerX = self.x - (self.width / 2)
            centerY = self.y - (self.height / 2)
            # cycle through our animations for drawing, i.e. explosions
            # for j in range(len(self.animations)):
            j = 0
            while j < len(self.animations):
                self.animations[j].draw(win)
                # remove any animations that have exceeded their durations
                if self.animations[j].attackAnimationStopTime < ticks:
                    del self.animations[j]
                j += 1
                    # continue

            # draw health bar and render sprite
            self.drawHealthBox(win, centerX, centerY)
            win.blit(self.image, (self.x - (self.width / 2), self.y - (self.height / 2)))


    # this is called when an enemy has hit a tower to reduce the towers health
    def hit(self, damage, damageType, ticks):
        self.health = self.health - damage
        self.damageTakenOnTurn += damage


    # parent stub for loading projectiles
    def loadProjectile(self, enemy):
        return Projectile((self.x, self.y), enemy, self.closeEnemies)


    # adds an animation for a projectile that has reached its target to the queue
    def addAnimationToQueue(self, projectile, ticks):
        animation = projectile.finalAnimation(projectile.enemyStartingPosition)
        animation.attackAnimationStopTime = ticks + animation.attackAnimationDuration
        self.animations.append(animation)
