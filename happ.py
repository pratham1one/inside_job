import pygame
import sys
import random

# Initialize Pygame
pygame.init()

#colour
red = 200
blue = 150
# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 40)

# Load your own images (replace with your files)
background = pygame.image.load("background.png").convert()
bird_img = pygame.image.load("bird.png").convert_alpha()
enemy_img = pygame.image.load("enemy.png").convert_alpha()
pipe_img = pygame.image.load("pipe.png").convert_alpha()

# Scale images (optional)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
bird_img = pygame.transform.scale(bird_img, (60, 30))
enemy_img = pygame.transform.scale(enemy_img, (60, 40))
pipe_img = pygame.transform.scale(pipe_img, (70, 400))

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Bird setup
bird_rect = bird_img.get_rect(center=(100, HEIGHT // 2))

# Enemy setup
enemy_list = []
SPAWNENEMY = pygame.USEREVENT
pygame.time.set_timer(SPAWNENEMY, 2000)  # enemy every 2 sec

# Pipe setup (only lower pipes)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE, 2500)  # pipe every 2.5 sec

def draw_background():
    screen.blit(background, (0, 0))

def draw_bird():
    screen.blit(bird_img, bird_rect)

def create_enemy():
    y_pos = random.randint(100, HEIGHT - 100)
    enemy = enemy_img.get_rect(midleft=(WIDTH + 50, y_pos))
    return enemy

def move_enemies(enemies):
    for e in enemies:
        e.centerx -= 5
    return [e for e in enemies if e.right > 0]

def draw_enemies(enemies):
    for e in enemies:
        screen.blit(enemy_img, e)

def create_pipe():
    y_pos = random.randint(300, HEIGHT - 50)
    pipe = pipe_img.get_rect(midtop=(WIDTH + 50, y_pos))
    return pipe

def move_pipes(pipes):
    for p in pipes:
        p.centerx -= 4
    return [p for p in pipes if p.right > 0]

def draw_pipes(pipes):
    for p in pipes:
        screen.blit(pipe_img, p)

def check_collision(enemies, pipes):
    # Enemy collision
    for e in enemies:
        if bird_rect.colliderect(e):
            return False
    # Pipe collision
    for p in pipes:
        if bird_rect.colliderect(p):
            return False
    # Ground / sky
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return False
    return True

def display_score(state):
    if state == "main_game":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
        screen.blit(score_surface, score_rect)
    if state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (0, 0 ))
        high_score_rect = high_score_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(high_score_surface, high_score_rect)

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                enemy_list.clear()
                pipe_list.clear()
                bird_rect.center = (100, HEIGHT // 2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNENEMY:
            enemy_list.append(create_enemy())

        if event.type == SPAWNPIPE:
            pipe_list.append(create_pipe())

    draw_background()

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        draw_bird()

        # Enemies
        enemy_list = move_enemies(enemy_list)
        draw_enemies(enemy_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Collision
        game_active = check_collision(enemy_list, pipe_list)

        # Score (add when enemies/pipes pass left of bird)
        for enemy in enemy_list:
            if enemy.centerx == bird_rect.centerx:
                score += 1
        for pipe in pipe_list:
            if pipe.centerx == bird_rect.centerx:
                score += 1

        display_score("main_game")

    else:
        high_score = max(high_score, score)
        display_score("game_over")

    pygame.display.update()
    clock.tick(60)
