import pygame
import random
import sys

pygame.init()

# --- Game Constants ---
WIDTH, HEIGHT = 400, 600
GAP = 160  # Gap between pipes
GRAVITY = 0.5
JUMP = -8
SPEED = 3

# --- Setup Screen ---
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# --- Load Assets ---
BIRD = pygame.image.load("assets/bird.png").convert_alpha()
PIPE = pygame.image.load("assets/pipe.png").convert_alpha()
BASE = pygame.image.load("assets/base.png").convert_alpha()
BG = pygame.image.load("assets/background.png").convert()

FONT = pygame.font.SysFont("Arial", 32)
CLOCK = pygame.time.Clock()

# --- Utility Functions ---
def draw_text(text, size, x, y, color=(255, 255, 255), center=False):
    font = pygame.font.SysFont("Arial", size)
    label = font.render(text, True, color)
    if center:
        rect = label.get_rect(center=(x, y))
        SCREEN.blit(label, rect)
    else:
        SCREEN.blit(label, (x, y))

def create_pipe():
    height = random.randint(150, 400)
    bottom_pipe = PIPE.get_rect(midtop=(WIDTH + 100, height + GAP // 2))
    top_pipe = PIPE.get_rect(midbottom=(WIDTH + 100, height - GAP // 2))
    return top_pipe, bottom_pipe

def draw_base(base_x):
    SCREEN.blit(BASE, (base_x, HEIGHT - BASE.get_height()))
    SCREEN.blit(BASE, (base_x + WIDTH, HEIGHT - BASE.get_height()))

def check_collision(bird_rect, pipes):
    for top_pipe, bottom_pipe in pipes:
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT - BASE.get_height():
        return True
    return False

# --- Main Game ---
def main_game():
    bird_rect = BIRD.get_rect(center=(50, HEIGHT // 2))
    bird_movement = 0

    base_x = 0
    pipes = []
    score = 0

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1200)
    pipes.append(create_pipe())

    running = True
    while running:
        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_movement = JUMP
            if event.type == SPAWNPIPE:
                pipes.append(create_pipe())

        # --- Bird Movement ---
        bird_movement += GRAVITY
        bird_rect.centery += int(bird_movement)

        # --- Pipe Movement ---
        new_pipes = []
        for top_pipe, bottom_pipe in pipes:
            top_pipe.centerx -= SPEED
            bottom_pipe.centerx -= SPEED
            if top_pipe.right > 0:
                new_pipes.append((top_pipe, bottom_pipe))
        pipes = new_pipes

        # --- Drawing ---
        SCREEN.blit(BG, (0, 0))

        for top_pipe, bottom_pipe in pipes:
            SCREEN.blit(pygame.transform.flip(PIPE, False, True), top_pipe)
            SCREEN.blit(PIPE, bottom_pipe)

        SCREEN.blit(BIRD, bird_rect)

        # --- Base ---
        base_x -= SPEED
        if base_x <= -WIDTH:
            base_x = 0
        draw_base(base_x)

        # --- Score ---
        for top_pipe, bottom_pipe in pipes:
            if top_pipe.centerx == bird_rect.centerx:
                score += 1
        draw_text(f"Score: {score}", 24, 10, 10)

        # --- Collision ---
        if check_collision(bird_rect, pipes):
            return score

        pygame.display.update()
        CLOCK.tick(60)

# --- Game Loop ---
while True:
    final_score = main_game()
    print(f"Game Over! Final Score: {final_score}")
