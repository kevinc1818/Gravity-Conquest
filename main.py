#SOURCE: http://programarcadegames.com/python_examples/show_file.php?file=move_with_walls_example.py

import pygame


#Player sprite
class Player(pygame.sprite.Sprite):
    #Initiates the player sprite
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.image = pygame.image.load("player3.png")

        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        #The list of walls in the game
        self.walls = None

    #Reverse gravity function
    def reverse_grav(self):
        pygame.mixer.music.load('swoosh.wav')
        pygame.mixer.music.play(0)
        global grav
        #Tests to see if player is touching ground to reverse gravity first
        if grav == 1:
            self.rect.y += 2
            block_hit_list = pygame.sprite.spritecollide(
                self, self.walls, False)
            self.rect.y -= 2
        elif grav == -1:
            self.rect.y -= 2
            block_hit_list = pygame.sprite.spritecollide(
                self, self.walls, False)
            self.rect.y += 2

        #Multiplies by -1 to get the opposite
        if len(block_hit_list) > 0:
            grav = grav * -1

        #Accelerates the gravity change
        if grav == 1:
            self.change_y = 5
        elif grav == -1:
            self.change_y = -5

    #Gravity calculation function
    def calc_grav(self):
        #Tests to see if player is on ground
        if grav == 1:
            self.rect.y += 2
            block_hit_list = pygame.sprite.spritecollide(
                self, self.walls, False)
            self.rect.y -= 2
        elif grav == -1:
            self.rect.y -= 2
            block_hit_list = pygame.sprite.spritecollide(
                self, self.walls, False)
            self.rect.y += 2

        #If player isn't on ground, accelerate player until they are touching ground
        if len(block_hit_list) == 0:
            if self.change_y == 0:
                self.change_y = grav * 1
            else:
                self.change_y += grav * .35

    #Jump function
    def jump(self):
        #Tests to see if player is on ground
        if grav == 1:
            self.rect.y += 2
            block_hit_list = pygame.sprite.spritecollide(
                self, self.walls, False)
            self.rect.y -= 2
        elif grav == -1:
            self.rect.y -= 2
            block_hit_list = pygame.sprite.spritecollide(
                self, self.walls, False)
            self.rect.y += 2

        #If player is on ground, then jump
        if len(block_hit_list) > 0:
            pygame.mixer.music.load('jump.wav')
            pygame.mixer.music.play(0)
            self.change_y = grav * -8

    #Move function (moves player)
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    #Update function
    def update(self):
        #Calculates gravity
        self.calc_grav()

        #Moves player horizontally regardless of walls
        self.rect.x += self.change_x

        #Tests if player hits a wall, if so, move it back
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        #Moves player vertically regardless of walls
        self.rect.y += self.change_y

        #Tests if player hits a wall, if so, move it back
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        #If player touches lava, the player dies (y axis)
        if grav == 1:
            self.rect.y += 2
            block_hit_list = pygame.sprite.spritecollide(
                self, death_list, False)
            self.rect.y -= 2
        elif grav == -1:
            self.rect.y -= 2
            block_hit_list = pygame.sprite.spritecollide(
                self, death_list, False)
            self.rect.y += 2
        if len(block_hit_list) > 0:
            self.die()

        #If player touches lava, the player dies (x axis)
        self.rect.x += 2
        block_hit_list = pygame.sprite.spritecollide(self, death_list, False)
        self.rect.x -= 2
        if len(block_hit_list) > 0:
            self.die()
        self.rect.x -= 2
        block_hit_list = pygame.sprite.spritecollide(self, death_list, False)
        self.rect.x += 2
        if len(block_hit_list) > 0:
            self.die()

        #Tests to see if player touches key, if so remove key and locked wall
        block_hit_list = pygame.sprite.spritecollide(self, key_list, False)
        if len(block_hit_list) > 0:
            pygame.mixer.music.load('coin.wav')
            pygame.mixer.music.play(0)
            all_sprite_list.remove(key_list)
            all_sprite_list.remove(lock_list)
            wall_list.remove(lock_list)
            pygame.sprite.Group.empty(key_list)

    #Death function
    def die(self):
        global grav
        global deathcount
        pygame.mixer.music.load('death.wav')
        pygame.mixer.music.play(0)
        resetLock()

        #Resets gravity and position when player dies
        grav = 1
        self.change_y = 0
        self.rect.x = 20
        self.rect.y = 500

        #Adds to death counter
        deathcount += 1

        #Key levels that need special resetting if player dies
        if level == 10:
            level10()

        if level == 13:
            level13()


#Wall sprite
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


#Lava sprite
class Death(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


#Locked wall sprite
class Lock(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 200, 0))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


#Key sprite
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 0))
        self.image = pygame.image.load("key2.png")
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


#Invisible wall sprite
class Invis(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


#Resets locked walls after player dies
def resetLock():
    all_sprite_list.add(lock_list)
    all_sprite_list.add(key_list)
    wall_list.add(lock_list)


#Initiation
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont("centurygothic", 60, bold=True)
smallfont = pygame.font.SysFont("centurygothic", 36, bold=True)
screen = pygame.display.set_mode((800, 800))
done = False
clock = pygame.time.Clock()

#Pictures
lvl = pygame.image.load('lvl.png')
lvl_black = pygame.image.load('lvl_black.png')
titlescreen = pygame.image.load('title.png')
menuscreen = pygame.image.load('menu.png')
winscreen = pygame.image.load('win.png')
death = pygame.image.load('death.png')
ins1 = pygame.image.load('instructions1.png')
ins2 = pygame.image.load('instructions2.png')
ins3 = pygame.image.load('instructions3.png')
ins4 = pygame.image.load('instructions4.png')
ins5 = pygame.image.load('instructions5.png')
ins6 = pygame.image.load('instructions6.png')
ins7 = pygame.image.load('instructions7.png')

#Levels 1-15


def level1():
    #Normal white wall
    wall = Wall(0, 750, 800, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)


def level2():
    wall = Wall(0, 750, 300, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(500, 750, 800, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)


def level3():
    wall = Wall(0, 750, 150, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(250, 750, 100, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(450, 750, 100, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(650, 750, 150, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    #Lava wall
    death = Death(150, 775, 100, 35)
    wall_list.add(death)
    death_list.add(death)
    all_sprite_list.add(death)

    death = Death(350, 775, 100, 35)
    wall_list.add(death)
    death_list.add(death)
    all_sprite_list.add(death)

    death = Death(550, 775, 100, 35)
    wall_list.add(death)
    death_list.add(death)
    all_sprite_list.add(death)


def level4():
    #More efficient way to create walls
    walls = [[0, 600, 50, 200], [100, 600, 45, 200], [200, 600, 40, 200],
             [300, 600, 35, 200], [400, 600, 30, 200], [500, 600, 25, 200],
             [600, 600, 20, 200], [700, 600, 15, 200], [790, 600, 10, 200]]

    for x in walls:
        wall = Wall(x[0], x[1], x[2], x[3])
        wall_list.add(wall)
        all_sprite_list.add(wall)


def level5():
    wall = Wall(0, 750, 250, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(550, 750, 250, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(250, 0, 300, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)


def level6():
    walls = [[0, 750, 50, 50], [200, 750, 50, 50], [250, 0, 50, 50],
             [475, 0, 50, 50], [550, 750, 50, 50], [750, 750, 50, 50]]

    for x in walls:
        wall = Wall(x[0], x[1], x[2], x[3])
        wall_list.add(wall)
        all_sprite_list.add(wall)

    death = Death(50, 775, 150, 35)
    wall_list.add(death)
    death_list.add(death)
    all_sprite_list.add(death)

    death = Death(300, 0, 175, 25)
    wall_list.add(death)
    death_list.add(death)
    all_sprite_list.add(death)

    death = Death(600, 775, 150, 35)
    wall_list.add(death)
    death_list.add(death)
    all_sprite_list.add(death)


def level7():
    walls = [[0, 775, 50, 25], [200, 75, 200, 25], [450, 150, 100, 25],
             [600, 225, 100, 25]]

    for x in walls:
        wall = Wall(x[0], x[1], x[2], x[3])
        wall_list.add(wall)
        all_sprite_list.add(wall)


def level8():
    walls = [[0, 750, 800, 50], [0, 0, 800, 50], [80, 100, 50, 700],
             [180, 50, 50, 650], [280, 100, 50, 700], [380, 50, 50, 650],
             [480, 100, 50, 700], [580, 50, 50, 650], [680, 100, 50, 700]]

    for x in walls:
        wall = Wall(x[0], x[1], x[2], x[3])
        wall_list.add(wall)
        all_sprite_list.add(wall)


def level9():
    walls = [[0, 750, 50, 50], [400, 750, 50, 50], [750, 750, 50, 50],
             [200, 0, 50, 50], [550, 0, 50, 50]]

    for x in walls:
        wall = Wall(x[0], x[1], x[2], x[3])
        wall_list.add(wall)
        all_sprite_list.add(wall)


def level10():
    walls = [[0, 750, 800, 50], [0, 0, 200, 50], [500, 550, 300, 50]]

    for x in walls:
        wall = Wall(x[0], x[1], x[2], x[3])
        wall_list.add(wall)
        all_sprite_list.add(wall)

    #Key
    key = Key(90, 75, 25, 25)
    key_list.add(key)
    screen.blit(key.image, key.rect)
    all_sprite_list.add(key)

    #Locked wall
    lock = Lock(500, 600, 50, 150)
    wall_list.add(lock)
    lock_list.add(lock)
    all_sprite_list.add(lock)


def level11():

    deaths = [[80, 100, 50, 700], [180, 50, 50, 650], [280, 100, 50, 700],
              [380, 50, 50, 650], [480, 100, 50, 700], [580, 50, 50, 650],
              [680, 100, 50, 700]]

    for x in deaths:
        death = Death(x[0], x[1], x[2], x[3])
        wall_list.add(death)
        death_list.add(death)
        all_sprite_list.add(death)

    walls = [[0, 750, 800, 50], [0, 0, 800, 50]]

    for x in walls:
        wall = Wall(x[0], x[1], x[2], x[3])
        wall_list.add(wall)
        all_sprite_list.add(wall)


def level12():
    wall = Wall(0, 750, 800, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    deaths = [
        [100, 735, 25, 15],
        [250, 720, 25, 30],
        [400, 705, 25, 45],
        [550, 690, 25, 60],
        [700, 675, 25, 75],
    ]

    for x in deaths:
        death = Death(x[0], x[1], x[2], x[3])
        wall_list.add(death)
        death_list.add(death)
        all_sprite_list.add(death)


def level13():
    walls = [
        [0, 750, 200, 50],
        [0, 0, 200, 50],
        [100, 0, 25, 50],
        [200, 0, 25, 50],
        [300, 0, 25, 50],
        [400, 0, 25, 50],
        [500, 0, 25, 50],
        [600, 0, 200, 50],
        [775, 0, 25, 700],
        [100, 750, 25, 50],
        [200, 750, 25, 50],
        [300, 750, 25, 50],
        [400, 750, 25, 50],
        [500, 750, 25, 50],
        [600, 750, 25, 50],
        [700, 750, 25, 50],
    ]

    for x in walls:
        wall = Wall(x[0], x[1], x[2], x[3])
        wall_list.add(wall)
        all_sprite_list.add(wall)

    key = Key(725, 100, 25, 25)
    key_list.add(key)
    screen.blit(key.image, key.rect)
    all_sprite_list.add(key)

    lock = Lock(775, 700, 25, 100)
    wall_list.add(lock)
    lock_list.add(lock)
    all_sprite_list.add(lock)

    death = Death(100, 400, 675, 25)
    wall_list.add(death)
    death_list.add(death)
    all_sprite_list.add(death)


def level14():
    #Invisible wall
    invis = Invis(300, 750, 200, 50)
    wall_list.add(invis)
    invis_list.add(invis)
    all_sprite_list.add(invis)

    wall = Wall(0, 750, 100, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(700, 750, 100, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)


def level15():
    invises = [[0, 750, 50, 50], [400, 750, 50, 50], [750, 750, 50, 50],
               [200, 0, 50, 50], [550, 0, 50, 50]]

    for x in invises:
        invis = Invis(x[0], x[1], x[2], x[3])
        wall_list.add(invis)
        invis_list.add(invis)
        all_sprite_list.add(invis)

    wall = Wall(0, 750, 75, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    wall = Wall(725, 750, 75, 50)
    wall_list.add(wall)
    all_sprite_list.add(wall)


#Next level function
def nextlevel():
    pygame.mixer.music.load('bleep.wav')
    pygame.mixer.music.play(0)
    global level
    global grav

    #Resets gravity and position after level has been beat
    grav = 1
    player.change_y = 0
    player.rect.x = 50
    player.rect.y = 500

    #Removes all sprites from the previous level apart from the player sprite
    all_sprite_list.remove(wall_list)
    pygame.sprite.Group.empty(wall_list)
    pygame.sprite.Group.empty(lock_list)
    pygame.sprite.Group.empty(key_list)
    pygame.sprite.Group.empty(death_list)
    pygame.sprite.Group.empty(invis_list)

    #Next level
    level += 1

    #Each level number corresponds to its function
    if level == 1:
        level1()
    elif level == 2:
        level2()
    elif level == 3:
        level3()
    elif level == 4:
        level4()
    elif level == 5:
        level5()
    elif level == 6:
        level6()
    elif level == 7:
        level7()
    elif level == 8:
        level8()
    elif level == 9:
        level9()
    elif level == 10:
        level10()
    elif level == 11:
        level11()
    elif level == 12:
        level12()
    elif level == 13:
        level13()
    elif level == 14:
        level14()
    elif level == 15:
        level15()


#Sprite group creation
all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
death_list = pygame.sprite.Group()
key_list = pygame.sprite.Group()
lock_list = pygame.sprite.Group()
invis_list = pygame.sprite.Group()

#Player sprite creation
player = Player(20, 500)
screen.blit(player.image, player.rect)
player.walls = wall_list
player.death = death_list
all_sprite_list.add(player)

#Variables
grav = 1
level = 0
state = 'title'
deathcount = 0

#Main body loop
while not done:
    #Get mouse position for buttons
    mousepos = pygame.mouse.get_pos()
    mousex = mousepos[0]
    mousey = mousepos[1]

    #Check to see if player has won
    if level == 16:
        state = 'win'
        pygame.sprite.Group.empty(all_sprite_list)

    #Test events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #Game controls
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-5, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(5, 0)
            elif event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_SPACE:
                player.reverse_grav()
            elif event.key == pygame.K_ESCAPE:
                state = 'menu'
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(5, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-5, 0)
        #Buttons
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Title screen
            if state == 'title':
                #Play button
                if mousex >= 167 and mousex <= 365 and mousey >= 588 and mousey <= 700:
                    state = 'game'

                    #Initiation variables
                    all_sprite_list = pygame.sprite.Group()
                    wall_list = pygame.sprite.Group()
                    death_list = pygame.sprite.Group()
                    key_list = pygame.sprite.Group()
                    lock_list = pygame.sprite.Group()
                    invis_list = pygame.sprite.Group()

                    #Creates sprite for player
                    player = Player(20, 500)
                    screen.blit(player.image, player.rect)
                    player.walls = wall_list
                    player.death = death_list
                    all_sprite_list.add(player)

                    grav = 1
                    nextlevel()

                #Menu button
                if mousex >= 445 and mousex <= 650 and mousey >= 588 and mousey <= 700:
                    state = 'menu'

            #Menu screen
            elif state == 'menu':
                #Initiation variables
                all_sprite_list = pygame.sprite.Group()
                wall_list = pygame.sprite.Group()
                death_list = pygame.sprite.Group()
                key_list = pygame.sprite.Group()
                lock_list = pygame.sprite.Group()
                invis_list = pygame.sprite.Group()

                #Creates sprite for player
                player = Player(20, 500)
                screen.blit(player.image, player.rect)
                player.walls = wall_list
                player.death = death_list
                all_sprite_list.add(player)

                grav = 1

                #Buttons for all 15 levels in the menu
                if mousex >= 50 and mousey >= 225 and mousex <= 165 and mousey <= 335:
                    level = 0
                    state = 'game'
                    nextlevel()
                if mousex >= 195 and mousey >= 225 and mousex <= 315 and mousey <= 335:
                    level = 1
                    state = 'game'
                    nextlevel()
                if mousex >= 335 and mousey >= 225 and mousex <= 460 and mousey <= 335:
                    level = 2
                    state = 'game'
                    nextlevel()
                if mousex >= 485 and mousey >= 225 and mousex <= 600 and mousey <= 335:
                    level = 3
                    state = 'game'
                    nextlevel()
                if mousex >= 630 and mousey >= 225 and mousex <= 750 and mousey <= 335:
                    level = 4
                    state = 'game'
                    nextlevel()
                if mousex >= 50 and mousey >= 385 and mousex <= 165 and mousey <= 490:
                    level = 5
                    state = 'game'
                    nextlevel()
                if mousex >= 195 and mousey >= 385 and mousex <= 315 and mousey <= 490:
                    level = 6
                    state = 'game'
                    nextlevel()
                if mousex >= 335 and mousey >= 385 and mousex <= 460 and mousey <= 490:
                    level = 7
                    state = 'game'
                    nextlevel()
                if mousex >= 485 and mousey >= 385 and mousex <= 600 and mousey <= 490:
                    level = 8
                    state = 'game'
                    nextlevel()
                if mousex >= 630 and mousey >= 385 and mousex <= 750 and mousey <= 490:
                    level = 9
                    state = 'game'
                    nextlevel()
                if mousex >= 50 and mousey >= 540 and mousex <= 165 and mousey <= 655:
                    level = 10
                    state = 'game'
                    nextlevel()
                if mousex >= 195 and mousey >= 540 and mousex <= 315 and mousey <= 655:
                    level = 11
                    state = 'game'
                    nextlevel()
                if mousex >= 335 and mousey >= 540 and mousex <= 460 and mousey <= 655:
                    level = 12
                    state = 'game'
                    nextlevel()
                if mousex >= 485 and mousey >= 540 and mousex <= 600 and mousey <= 655:
                    level = 13
                    state = 'game'
                    nextlevel()
                if mousex >= 630 and mousey >= 540 and mousex <= 750 and mousey <= 655:
                    level = 14
                    state = 'game'
                    nextlevel()

            #Winning screen
            elif state == 'win':
                #Menu button
                if mousex >= 290 and mousey >= 535 and mousex <= 500 and mousey <= 650:
                    level = 0
                    state = 'menu'

    #Tests to see if player is outside of screen (left, bottom, top), if so, kill player
    if player.rect.x < 0 or player.rect.y > 800 or player.rect.y < 0:
        player.die()

    #Tests to see if player is on the right side of the screen
    if player.rect.x > 790:
        nextlevel()

    #Updates all of the sprites
    all_sprite_list.update()
    screen.fill((0, 0, 0))

    #Puts the background images for title, menu, and winning screen and puts 'level' in top left corner
    if state == 'game':
        screen.blit(lvl, (3, 3))
    elif state == 'title':
        pygame.sprite.Group.empty(all_sprite_list)
        screen.blit(titlescreen, (0, 0))
    elif state == 'menu':
        level = 0
        deathcount = 0
        pygame.sprite.Group.empty(all_sprite_list)
        screen.blit(menuscreen, (0, 0))
    elif state == 'win':
        pygame.sprite.Group.empty(all_sprite_list)
        screen.blit(winscreen, (0, 0))
        screen.blit(death, (350, 700))
        textsurface = smallfont.render(str(deathcount), False, (255, 255, 255))
        if deathcount > 99:
            screen.blit(textsurface, (275, 695))
        else:
            screen.blit(textsurface, (300, 695))

    #Different instructions and level numbers for each of the levels
    if level == 1:
        screen.blit(ins1, (250, 350))
        textsurface = myfont.render('1', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 2:
        screen.blit(ins2, (250, 350))
        textsurface = myfont.render('2', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 3:
        screen.blit(ins3, (250, 350))
        textsurface = myfont.render('3', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 4:
        textsurface = myfont.render('4', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 5:
        screen.blit(ins4, (250, 350))
        textsurface = myfont.render('5', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 6:
        textsurface = myfont.render('6', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 7:
        textsurface = myfont.render('7', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 10:
        screen.blit(ins5, (250, 350))
    elif level == 12:
        textsurface = myfont.render('12', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 14:
        screen.blit(ins6, (250, 350))
        textsurface = myfont.render('14', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))
    elif level == 15:
        screen.blit(ins7, (250, 350))

    #Draws all of the sprites onto screen (player, walls, etc.)
    all_sprite_list.draw(screen)

    #Some levels go after sprites, ex: level is black and goes over a wall
    if level == 8:
        screen.blit(lvl_black, (3, 0))
        textsurface = myfont.render('8', False, (0, 0, 0))
        screen.blit(textsurface, (200, -15))
    elif level == 9:
        textsurface = myfont.render('9', False, (0, 0, 0))
        screen.blit(textsurface, (200, -10))
    elif level == 10:
        screen.blit(lvl_black, (3, 0))
        textsurface = myfont.render('10', False, (255, 255, 255))
        screen.blit(textsurface, (200, -15))
    elif level == 11:
        screen.blit(lvl_black, (3, 0))
        textsurface = myfont.render('11', False, (0, 0, 0))
        screen.blit(textsurface, (200, -13))
    elif level == 13:
        screen.blit(lvl_black, (3, 0))
        textsurface = myfont.render('1', False, (0, 0, 0))
        screen.blit(textsurface, (200, -15))
        textsurface = myfont.render('3', False, (255, 255, 255))
        screen.blit(textsurface, (230, -15))
    elif level == 15:
        textsurface = myfont.render('15', False, (255, 255, 255))
        screen.blit(textsurface, (200, -10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
