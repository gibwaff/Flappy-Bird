import pygame
import random


clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Super Game')


# icon = pygame.image.load(image_path + 'sprites/boxes-512.webp')
# pygame.display.set_icon(icon)

class Collon:
    def __init__(self, number, rect):
        self.number = number
        self.rect = rect
        self.passed = False

label = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 50)
support_label = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 30)
label_over = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 60)

lose_label = label_over.render('Game Over!', False, (240, 248, 255))
restart_label = label_over.render('Play Again', False, (240, 248, 255))
start_label = support_label.render('Press "Space" to start', False, (240, 248, 255))

restart_label_rect = restart_label.get_rect(topleft=(310, 300))

bg = pygame.image.load('sprites/background.png').convert_alpha()
bg_x = 0

top_collons = [
    pygame.image.load('sprites/collons/top_collons/top_col_70.png').convert_alpha(),
    pygame.image.load('sprites/collons/top_collons/top_col_110.png').convert_alpha(),
    pygame.image.load('sprites/collons/top_collons/top_col_140.png').convert_alpha(),
    pygame.image.load('sprites/collons/top_collons/top_col_185.png').convert_alpha(),
    pygame.image.load('sprites/collons/top_collons/top_col_225.png').convert_alpha(),
    pygame.image.load('sprites/collons/top_collons/top_col_250.png').convert_alpha(),
    pygame.image.load('sprites/collons/top_collons/top_col_300.png').convert_alpha(),
    pygame.image.load('sprites/collons/top_collons/top_col_330.png').convert_alpha()
]
bot_collons = [
    pygame.image.load('sprites/collons/bot_collons/bot_col_330.png').convert_alpha(),
    pygame.image.load('sprites/collons/bot_collons/bot_col_290.png').convert_alpha(),
    pygame.image.load('sprites/collons/bot_collons/bot_col_260.png').convert_alpha(),
    pygame.image.load('sprites/collons/bot_collons/bot_col_215.png').convert_alpha(),
    pygame.image.load('sprites/collons/bot_collons/bot_col_175.png').convert_alpha(),
    pygame.image.load('sprites/collons/bot_collons/bot_col_150.png').convert_alpha(),
    pygame.image.load('sprites/collons/bot_collons/bot_col_100.png').convert_alpha(),
    pygame.image.load('sprites/collons/bot_collons/bot_col_70.png').convert_alpha()
]
top_collons_ingame = []
bot_collons_ingame = []

col_timer = pygame.USEREVENT + 1
pygame.time.set_timer(col_timer, 1500)

bird = pygame.image.load('sprites/Flappy Bird.png').convert_alpha()
b_x = 350
b_y = 250
g = 0.08
canjump = True
jump = False
up = 8
bird_rect = bird.get_rect(topleft=(b_x, b_y))

start = False
score = 0

gaming = True
running = True
while running:
    if gaming:
        keys = pygame.key.get_pressed()

        screen.blit(bg, (bg_x, 0))
        if bg_x <= -304:
            bg_x = -3
        else:
            bg_x -= 3

        if top_collons_ingame:
            for el in top_collons_ingame:
                screen.blit(top_collons[el.number], (el.rect.x, el.rect.y))
                el.rect.x -= 3
                if bird_rect.x in range(el.rect.x, el.rect.x + 10) and not el.passed:
                    score += 1
                    el.passed = True
                if bird_rect.colliderect(el.rect):
                    gaming = False


            top_collons_ingame = [el for el in top_collons_ingame if el.rect.x > -100]
        if bot_collons_ingame:
            for el in bot_collons_ingame:
                screen.blit(bot_collons[el.number], (el.rect.x, el.rect.y))
                el.rect.x -= 3
                if bird_rect.colliderect(el.rect):
                    gaming = False

            bot_collons_ingame = [el for el in bot_collons_ingame if el.rect.x > -100]

        screen.blit(bird, (bird_rect.x, bird_rect.y))
        bird_rect.y += g
        if start:
            g += 0.25
        if jump:
            g = 0.08
            bird_rect.y -= up
            up -= 0.5
            if up <= 3:
                canjump = True
            if up <= 0:
                jump = False

        if bird_rect.y >= 520 or bird_rect.y <= 0:
            gaming = False

        if start:
            score_label = label.render(str(score), False, (240, 248, 255))
            screen.blit(score_label, (550, 50))
        if not start:
            screen.blit(start_label, (260, 350))

    else:
        screen.blit(lose_label, (310, 150))
        screen.blit(restart_label, (310, 300))

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gaming = True
            bird_rect.x = 350
            bird_rect.y = 250
            g = 0.08
            canjump = True
            jump = False
            up = 8
            score = 0
            top_collons_ingame.clear()
            bot_collons_ingame.clear()
            start = False



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == col_timer and start:
            num = random.randrange(8)
            top_col = Collon(num, top_collons[num].get_rect(topleft=(1250, 0)))
            top_collons_ingame.append(top_col)
            bot_col = Collon(num, bot_collons[num].get_rect(bottomleft=(1250, 550)))
            bot_collons_ingame.append(bot_col)

        if canjump and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            jump = True
            canjump = False
            up = 8
            start = True

    clock.tick(60)


