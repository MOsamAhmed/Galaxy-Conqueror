"""
Note #1:
In some IDE(s), for example in Visual Studio Code sometimes, when
using pygame module and trying to access some of its function it shows
error that no such function is available but in reality its available.
And when we run the program it does not crash or give an error.

Note #2:
Also in VS Code don't directly open the file because in that way it
does not load the resources. Open the folder in IDE where the assets folder and
game.py file are present. So in that way VS Code load the assets folder.

Note #2:
In order to run this program we have to install pygame module.
The pip command for that module is:
pip install pygame
"""

import pygame
import random
from pygame import mixer

# Initializing All Pygame Modules.
pygame.init()

# Importing pygame clock to manage fps.
clock = pygame.time.Clock()

# Create The Screen.
screen = pygame.display.set_mode((800, 600))

# Background.
bg = pygame.image.load('assets\\images\\bg.png')
menu_bg = pygame.image.load('assets\\images\\main menu bg.png')
game_over_bg = pygame.image.load('assets\\images\\game over bg.png')

# Background Sound.
mixer.music.load('assets\\audio\\Call of Duty - acappella - Live Voices.wav')
mixer.music.play(-1)

# Title & Icon.
pygame.display.set_caption('Galaxy Conqueror')
icon = pygame.image.load('assets\\images\\icon.png')
pygame.display.set_icon(icon)

# Player.
player_img = pygame.image.load('assets\\images\\player.png')
player_x = 368  # Max-(728), Min-(8)
player_y = 475  # Max-(528), Min-(308)
player_x_change = 0

# Enemies.
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = 25
num_of_enemies = 5

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('assets\\images\\enemy.png'))
    enemy_x.append(random.randint(73, 663))  # Max-(728), Min-(8)
    enemy_y.append(random.randint(42, 158))  # Max-(292), Min-(42)
    enemy_x_change.append(3 * random.randrange(-1, 2, 2))

# Bullet.
bullet_img = pygame.image.load('assets\\images\\bullet.png')
bullet_x = 0
bullet_y = 475
bullet_y_change = 12.5
# Ready - When the bullet can't be seen.
# Fire - When the bullet is moving.
bullet_state = 'Ready'

# Score.
score = 0
score_font1 = pygame.font.Font('assets\\fonts\\Youthanasia.ttf', 33)
score_font2 = pygame.font.Font('assets\\fonts\\Youthanasia.ttf', 32)


# Functions:
def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, enemy_index):
    screen.blit(enemy_img[enemy_index], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'Fire'
    screen.blit(bullet_img, (x + 16, y - 10))


def is_collision(e_x, e_y, b_x, b_y):
    distance = ((e_x - b_x) ** 2 + (e_y - b_y) ** 2) ** 0.5
    if distance < 40:
        return True
    else:
        return False


def show_score():
    score_img1 = score_font1.render(f'Score: {score}', True, (0, 0, 0))
    score_img2 = score_font2.render(f'Score: {score}', True, (48, 18, 174))
    screen.blit(score_img1, (7, 10))
    screen.blit(score_img2, (10, 10))


# Game Loop Prerequisites.
running = True
menu = True
respawn_characters = False
end = False

# Game Loop.
while running:
    # Game Menu.
    while menu:

        screen.blit(menu_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    respawn_characters = True
                    menu = False

        # Updating Display/Frame.
        pygame.display.update()

    if respawn_characters is True:
        # Enemies Creating.
        enemy_img = []
        enemy_x = []
        enemy_y = []
        enemy_x_change = []
        enemy_y_change = 25
        num_of_enemies = 5

        for i in range(num_of_enemies):
            enemy_img.append(pygame.image.load('assets\\images\\enemy.png'))
            enemy_x.append(random.randint(73, 663))  # Max-(728), Min-(8)
            enemy_y.append(random.randint(42, 158))  # Max-(292), Min-(42)
            enemy_x_change.append(4 * random.randrange(-1, 2, 2))

        score = 0
        respawn_characters = False

    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke Checking, Left or Right or Space.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'Ready':  # We can also use this condition (if bullet_y == 475:)
                    bullet_state = 'Fire'
                    bullet_x = player_x
                    # Bullet Sound.
                    bullet_sound = mixer.Sound('assets\\audio\\laser.wav')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_x_change = 0

    # Checking Boundaries For Player.
    player_x += player_x_change
    if player_x > 728:
        player_x = 728
    elif player_x < 8:
        player_x = 8
    player(player_x, player_y)

    # Movement Of Enemies.
    for i in range(num_of_enemies):

        # Checking Game Over.
        if enemy_y[i] > 425:
            # Game Over Sound.
            game_over_sound = mixer.Sound('assets\\audio\\game over.wav')
            game_over_sound.play()
            end = True
            while end and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        menu = False
                        end = False
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            menu = True
                            end = False

                screen.blit(game_over_bg, (0, 0))
                # Displaying Score.
                show_score()
                pygame.display.update()

        enemy_x[i] += enemy_x_change[i]
        # Checking Enemies Boundary.
        if enemy_x[i] >= 728:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change
        elif enemy_x[i] <= 8:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change
        enemy(enemy_x[i], enemy_y[i], i)

        # Checking collision.
        if bullet_state == 'Fire':
            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                bullet_state = 'Ready'
                bullet_y = 475
                score += 1
                # Respawning Enemy.
                enemy_x[i] = random.randint(8, 728)  # Max-(728), Min-(8)
                enemy_y[i] = random.randint(42, 158)  # Max-(292), Min-(42)
                enemy_x_change[i] = 3 * random.randrange(-1, 2, 2)
                # Collision Sound.
                collision_sound = mixer.Sound('assets\\audio\\explosion.wav')
                collision_sound.play()

    # Movement Of Bullet.
    if bullet_state == 'Fire':
        if bullet_y <= -16:
            bullet_state = 'Ready'
            bullet_y = 475
        else:
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

    # Displaying Score.
    show_score()

    # Updating Display/Frame.
    if menu is False:
        pygame.display.update()
        clock.tick(60)  # To manage fps.
