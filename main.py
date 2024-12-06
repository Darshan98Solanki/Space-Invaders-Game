import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))
running = True

# backgroung sound
mixer.music.load("music/background.wav")
mixer.music.play(-1)

# background
background = pygame.image.load("images/background.gif")
background = pygame.transform.scale(background, (800, 600))

# change the title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("images/icon.jpg")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load("images/player.png")
playerimg = pygame.transform.scale(playerimg, (50, 50))
playerX = 370
playerY = 480
playerX_change = 0

# ready - bullet is ready but don't fire yet
# fire - bullet if currentl moving on screen
# bullet
bulletimg = pygame.image.load("images/bullet.png")
bulletimg = pygame.transform.scale(bulletimg, (40, 30))
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = 0.6
bullet_state = "ready"

# playagain image
play_again_img = pygame.image.load("images/playagain.png").convert_alpha()
play_again_img = pygame.transform.scale(play_again_img, (170, 60))

# exit
exit_img = pygame.image.load("images/exit.png").convert_alpha()
exit_img = pygame.transform.scale(exit_img, (170, 60))


# button class
class Button():
    def __init__(self, x, y, image):
        height = image.get_height()
        width = image.get_width()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


play_again = Button(240, 360, play_again_img)
exit = Button(410, 360, exit_img)

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load("images/enemy2.png"))
    enemyX.append(random.randint(0, 745))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(30)

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 26)

textX = 10
textY = 10

# GameOver
gameover = pygame.image.load("images/gameover.png")
gameover = pygame.transform.scale(gameover, (350, 300))

addenemyflag = True


def game_over():
    global running, playerX, playerY, playerX_change, bulletY, num_of_enemy, bulletX, bulletY, bullet_state, enemyY, enemyX, score
    screen.blit(gameover, (250, 120))
    gameover.set_alpha(255)
    play_again_img.set_alpha(255)
    exit_img.set_alpha(255)
    bulletY = -1
    if play_again.draw():
        gameover.set_alpha(0)
        play_again_img.set_alpha(0)
        exit_img.set_alpha(0)
        num_of_enemy = 6
        playerX = 370
        playerY = 480
        playerX_change = 0
        bulletX = 370
        bulletY = 480
        bullet_state = "ready"
        score = 0
        for k in range(num_of_enemy):
            enemyX[k] = (random.randint(0, 745))
            enemyY[k] = (random.randint(50, 150))
            enemy(enemyX[k], enemyY[k], k)
    if exit.draw():
        running = False


def show_score(x, y):
    showscore = font.render("Score : " + str(score), True, (255, 110, 220))
    screen.blit(showscore, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 6, y + 10))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance <= 30:
        return True
    else:
        return False


def addenemy():
    global addenemyflag
    if addenemyflag:
        enemyimg.append(pygame.image.load("images/enemy2.png"))
        enemyX.append(random.randint(0, 745))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(0.3)
        enemyY_change.append(30)
        addenemyflag = False


# game loop for our gaming window
while running:
    # change color of a screen
    screen.fill((0, 0, 0))
    # add background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # moving a player usinng key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # add laser sound
                    laser_sound = mixer.Sound("music/laser.wav")
                    laser_sound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # make the boundaries for spaceship and enemy
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750

    if score % 10 == 0 and addenemyflag and score != 0:
        num_of_enemy += 1
        addenemy()

    for i in range(num_of_enemy):

        # Game Over
        if enemyY[i] > 445:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 745:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # add explosion sound
            explosion_sound = mixer.Sound("music/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            addenemyflag = True
            enemyX[i] = random.randint(0, 745)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
