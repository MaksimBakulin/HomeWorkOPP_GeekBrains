import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Bakulio")
icon = pygame.image.load("image/icon.png").convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load("image/bg.png").convert_alpha()
walk_right = [
    pygame.image.load("image/player_right/player_right1.png").convert_alpha(),
    pygame.image.load("image/player_right/player_right2.png").convert_alpha(),
    pygame.image.load("image/player_right/player_right3.png").convert_alpha(),
    pygame.image.load("image/player_right/player_right4.png").convert_alpha(),
    pygame.image.load("image/player_right/player_right5.png").convert_alpha(),
    pygame.image.load("image/player_right/player_right6.png").convert_alpha()
]
walk_left = [
    pygame.image.load("image/player_left/player_left1.png").convert_alpha(),
    pygame.image.load("image/player_left/player_left2.png").convert_alpha(),
    pygame.image.load("image/player_left/player_left3.png").convert_alpha(),
    pygame.image.load("image/player_left/player_left4.png").convert_alpha(),
    pygame.image.load("image/player_left/player_left5.png").convert_alpha(),
    pygame.image.load("image/player_left/player_left6.png").convert_alpha()
]

walk_enemy_agent = [
    pygame.image.load("image/enemy/enemy_left1.png").convert_alpha(),
    pygame.image.load("image/enemy/enemy_left2.png").convert_alpha(),
    pygame.image.load("image/enemy/enemy_left3.png").convert_alpha(),
    pygame.image.load("image/enemy/enemy_left4.png").convert_alpha(),
    pygame.image.load("image/enemy/enemy_left5.png").convert_alpha(),
    pygame.image.load("image/enemy/enemy_left6.png").convert_alpha()
]
enemy_list = []

enemy_anim_count = 0
player_anim_count = 0
bg_x = 0

player_speed = 15
player_x = 150
player_y = 550

is_jump = False
jump_count = 13

bg_sound = pygame.mixer.Sound("music/background.mp3")
bg_sound.play()

enemy_agent_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_agent_timer, 5000)

label = pygame.font.Font("fonts/Yellowtail-Regular.ttf", 100)
lose_label = label.render("You lose", False, (193, 196, 199))
restart_label = label.render("Try again", False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))
bullets_left = 5
bullet = pygame.image.load("image/bullet.png").convert_alpha()
bullets = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1920, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))


        if enemy_list:
            for (i, el) in enumerate(enemy_list):
                screen.blit(walk_enemy_agent[enemy_anim_count], el)
                enemy_rect = walk_enemy_agent[0].get_rect(topleft=(el.x, el.y))
                el.x -= 10

            if el.x < -10:
                    enemy_list.pop(i)

            if player_rect.colliderect(el):
                gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 10:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1780:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -13:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 13

        if enemy_anim_count == 5:
            enemy_anim_count = 0
        else:
            enemy_anim_count += 1

        if player_anim_count == 5:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 5
        if bg_x == -1920:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 40

                if el.x > 1920:
                    bullets.pop(i)

                if enemy_list:
                    for (index, enemy) in enumerate(enemy_list):
                        if el.colliderect(enemy_rect):
                            enemy_list.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            enemy_list.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_agent_timer:
            enemy_list.append(walk_enemy_agent[0].get_rect(topleft=(1950, 550)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_q and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 200, player_y + 130)))
            bullets_left -= 1

    clock.tick(15)