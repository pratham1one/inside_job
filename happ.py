import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 200, 300
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Plane")

# Game settings (slower & easier)
GRAVITY = 0.4    # slower falling
JUMP = -7        # softer jump
GAP = 80         # gap between top and bottom pipe
SPEED = 2        # slower horizontal movement
FONT = pygame.font.SysFont("Arial", 18)
BIG_FONT = pygame.font.SysFont("Arial", 28)

clock = pygame.time.Clock()

# Load and scale images
BIRD = pygame.image.load("assets/plane-2 copy.webp").convert_alpha()  # PNG with transparency
BIRD = pygame.transform.scale(BIRD, (34, 24))

PIPE = pygame.image.load("assets/pipe.png").convert_alpha()
PIPE = pygame.transform.scale(PIPE, (40, HEIGHT))

BASE = pygame.image.load("assets/base.png").convert_alpha()
BASE = pygame.transform.scale(BASE, (WIDTH, 40))

BG = pygame.image.load("assets/1950.jpg").convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

def draw_text(text, x, y, font=FONT, color=(255, 255, 255)):
    score_surface = font.render(text, True, color)
    SCREEN.blit(score_surface, (x, y))

def create_pipe():
    """Create a pair of pipes with random vertical position."""
    height = random.randint(50, HEIGHT - 50 - GAP)
    top = PIPE.get_rect(midbottom=(WIDTH + 40, height))
    bottom = PIPE.get_rect(midtop=(WIDTH + 40, height + GAP))
    return top, bottom

def main():
    bird_y = HEIGHT // 2
    bird_movement = 0
    bird_rect = BIRD.get_rect(center=(50, bird_y))

    pipes = []
    score = 0
    base_x = 0

    # Pipe spawn timer (slower = more time to react)
    pipe_timer = pygame.USEREVENT
    pygame.time.set_timer(pipe_timer, 1400)
    pipes.extend(create_pipe())

    running = True
    while running:
        SCREEN.blit(BG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_movement = JUMP

            if event.type == pipe_timer:
                pipes.extend(create_pipe())

        # Bird movement
        bird_movement += GRAVITY
        bird_rect.centery += int(bird_movement)
        SCREEN.blit(BIRD, bird_rect)

        # Pipes with collision check fixed
        new_pipes = []
        for pipe in pipes:
            pipe.centerx -= SPEED

            if pipe.bottom >= HEIGHT:  # bottom pipe
                SCREEN.blit(PIPE, pipe)
                if bird_rect.colliderect(pipe):
                    game_over_screen(score)
                    return
            else:  # top pipe flipped
                flipped_pipe = pygame.transform.flip(PIPE, False, True)
                SCREEN.blit(flipped_pipe, pipe)
                if bird_rect.colliderect(pipe):
                    game_over_screen(score)
                    return

            if pipe.right > 0:
                new_pipes.append(pipe)
        pipes = new_pipes

        # Score update
        for pipe in pipes:
            if pipe.centerx == bird_rect.centerx:
                score += 0.5  # 0.5 per pipe, 1 per pair
        draw_text(f"Score: {int(score)}", 10, 10)

        # Collision with top/bottom of screen
        if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT - BASE.get_height():
            game_over_screen(score)
            return  # Game over

        # Move base
        base_x -= SPEED
        if base_x <= -WIDTH:
            base_x = 0
        SCREEN.blit(BASE, (base_x, HEIGHT - BASE.get_height()))
        SCREEN.blit(BASE, (base_x + WIDTH, HEIGHT - BASE.get_height()))

        pygame.display.update()
        clock.tick(60)

def game_over_screen(final_score):
    """Display the Game Over screen and wait for restart."""
    SCREEN.blit(BG, (0, 0))
    draw_text("GAME OVER", 40, HEIGHT // 2 - 40, BIG_FONT, (255, 0, 0))
    draw_text(f"Score: {int(final_score)}", 60, HEIGHT // 2, FONT)
    draw_text("Press SPACE to restart", 15, HEIGHT // 2 + 40, FONT)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Run the game in a loop
while True:
    main()

