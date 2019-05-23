import pygame

class Tower:
    def __init__(self, position):
        self.x = position[0]   #Position on map
        self.y = position[1]
        self.damage = 0        #Amount of damage delt per attack
        self.attackRadius = 0  #Distance it can attach enemies from
        self.coolDown = 1000   #Time between attacks in ms
        self.canAttackTime = 0 #Timestamp showing when tower can attack again
        self.image = None      #Current image being displayed
        self.width = 64        #Width of animation images
        self.height = 64       #Height of animation images


    def attack(self, enemies):
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
                enemies[closestEnemyIndex].hit(self.damage)
                self.canAttackTime = ticks + self.coolDown
        return enemies


    def draw(self, win):
        ''' Render the tower to the map '''
        centerX = self.x - (self.width / 2)
        centerY = self.y - (self.height / 2)
        win.blit(self.image, (centerX, centerY))
