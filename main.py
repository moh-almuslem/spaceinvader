import pygame
import random
import math

# from pygame import mixer (for music)
# initialize pygame
pygame.init()
# create game window
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("space.png")

# Background music
# mixer.music.load("background.wav")
# mixer.music.play(-1), -1 to play on repeat

# Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('umbreon.png')
pygame.display.set_icon(icon)

# Player
playerImg = icon = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
# Ready - can't see bullet
# Fire - bullet moving
bulletImg = icon = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# Game Over text

game_over = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (225, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    GAME_OVER = game_over.render("GAME OVER", True, (225, 255, 255))
    screen.blit(GAME_OVER, (200, 250))


def player(x, y):
    # blit draws image
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit draws image
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


def Gover(enemyX, enemyY, playerX, playerY):
    dist = math.sqrt(math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2))
    if dist < 27:
        return True
    else:
        return False


# Game loop
running = True

while running:
    # RGB setup RED, Green , BLue (255 max)
    screen.fill((0, 0, 0))
    # background img
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed, check which one.
        # KEYDOWN checks if pressed.
        # KEYUP checks if button is released.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # bullet_sound = mixer.Sound(".wav")
                    # bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # setting up the player's movement boundaries
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # setting up the enemy's movement boundaries
    for i in range(num_of_enemies):

        # Game Over

        d = Gover(enemyX[i], enemyY[i], playerX, playerY)
        if d:
            #enemyY[i] = 2000

            enemy(2000, 2000, ' ')
            #enemyImg[i] = False
            game_over_text()
            # for j in range(num_of_enemies):
            #    enemyY[j] = 2000
            # game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collide = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collide:
            # explosion_sound = mixer.Sound(".wav")
            # explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
