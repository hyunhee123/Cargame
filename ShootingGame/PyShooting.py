import pygame
import sys
import random
from time import sleep


padWidth = 480  #Width in Game
padHeight = 640 #Height in Game
rockImage = ['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
             'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
             'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
             'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
             'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
             'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png'] 
explosionSound = ['explosion01.wav', 'explosion02.wav','explosion03.wav','explosion04.wav']

# Destroying score
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('Destroyed:' + str(count), True, (255,255,255))
    gamePad.blit(text,(10,0))

# Rock past to the bottom
def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('Missed:' + str(count), True, (255,0,0))
    gamePad.blit(text, (360,0))

# Game Message
def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('NanumGothic.ttf', 80)
    text = textfont.render(text, True,  (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop() # Music stops
    gameOverSound.play() # Gameover sound plays
    sleep(2)
    pygame.mixer.music.play(-1) # Play background music
    runGame()

# Message when rock hit the fighter
def crash():
    global gamePad
    writeMessage('Destroyed!')

# Game over Message
def gameOver():
    global gamePad
    writeMessage('Game Over!')


#Draw Object
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame. display.set_caption('PyShooting') #Name of the game
    background = pygame.image.load('background.png') #Background Picture
    fighter = pygame.image.load('fighter.png') #Picture of fighter
    missile = pygame.image.load('missile.png') #Picture of missile
    explosion = pygame.image.load('explosion.png') #Picture of explosion
    pygame.mixer.music.load('music.wav') # Background music
    pygame.mixer.music.play(-1) #Play Background music
    missileSound = pygame.mixer.Sound('missile.wav') #Missile Sound
    gameOverSound = pygame.mixer.Sound('gameover.wav') #Gameover Sound
    clock = pygame.time.Clock()


def runGame():
    global gamepad, clock, background, fighter, missile, explosion, missileSound

    # Size of fighter
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # fighter first place
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    # Weapon location List
    missileXY = []

    # Random rock appears
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size # Rock Size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    # Rock first location
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    # When hit by rock True
    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:  #Quit game
                pygame.quit()
                sys.exit()
            # move the fighter to the left
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5
            # move the fighter to the right
                elif event.key == pygame.K_RIGHT:
                    fighterX += 5
            # Shoot missile
                elif event.key == pygame.K_SPACE:
                    missileSound.play() # missile sound play
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            # Figter stops when release the button
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0) #Draw background

        # Relocate the fighter
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        # Check if the fighter crashed the rock
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or \
                    (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()

        drawObject(fighter, x, y) # Drop the fighter

        # Draw shooting missile
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): #repeat missile factor
                bxy[1] -= 10 # shooting y -10 (moving up)
                missileXY[i][1] = bxy[1]

                # When missile hitted the rock
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0: #if missile move out from the screen
                    try:
                        missileXY.remove(bxy) #remove missile
                    except:
                        pass
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        # Rock hit
        writeScore(shotCount)

        rockY += rockSpeed # Rock moves down
        # When rock dropped down to the Earth
        if rockY > padHeight:
            # New Rock (Random)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        # When misses three rocks game over
        if rockPassed == 3:
            gameOver()

        
        writePassed(rockPassed)

        if isShot:
            drawObject(explosion, rockX, rockY) # Draw rock explosion
            destroySound.play() # Rock explosion sound

            # New Rock (Random)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False
            # Rock speed increases
            rockSpeed += 0.2
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY) #draw Rock

        pygame.display.update() #redraw game background

        clock.tick(60) #Frame 60 per second

    pygame.quit() #pygame ends

initGame()
runGame()


