import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
BIRD = pygame.image.load("assets/plane.jpeg")
PIPE = pygame.image.load("assets/pipe.png")
BASE = pygame.image.load("assets/base.png")
BG = pygame.image.load("assets/1950.jpg")

# Game settings
GRAVITY = 0.5
JUMP = -8
GAP = 150
SPEED = 3
FONT = pygame.font.SysFont("Arial", 32)

clock = pygame.time.Clock()

def draw_text(text, x, y):
    score_surface = FONT.render(text, True, (255, 255, 255))
    SCREEN.blit(score_surface, (x, y))

def main():
    bird_y = HEIGHT // 2
    bird_movement = 0
    bird_rect = BIRD.get_rect(center=(50, bird_y))

    pipes = []
    score = 0
    base_x = 0

    def create_pipe():
        height = random.randint(150, 400)
        top = PIPE.get_rect(midbottom=(WIDTH + 100, height - GAP // 2))
        bottom = PIPE.get_rect(midtop=(WIDTH + 100, height + GAP // 2))
        return top, bottom

    pipe_timer = pygame.USEREVENT
    pygame.time.set_timer(pipe_timer, 1200)
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

        # Pipes
        new_pipes = []
        for pipe in pipes:
            pipe.centerx -= SPEED
            if pipe.bottom >= HEIGHT:  # bottom pipe
                SCREEN.blit(PIPE, pipe)
            else:  # top pipe (flipped)
                flipped_pipe = pygame.transform.flip(PIPE, False, True)
                SCREEN.blit(flipped_pipe, pipe)

            if pipe.right > 0:
                new_pipes.append(pipe)

        pipes = new_pipes

        # Score update
        for pipe in pipes:
            if pipe.centerx == bird_rect.centerx:
                score += 0.5  # each pipe pair = 1 point (0.5 + 0.5)
        draw_text(f"Score: {int(score)}", 10, 10)

        # Collision detection
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                return  # Game over

        if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT - BASE.get_height():
            return  # Game over

        # Move base
        base_x -= SPEED
        if base_x <= -WIDTH:
            base_x = 0
        SCREEN.blit(BASE, (base_x, HEIGHT - BASE.get_height()))
        SCREEN.blit(BASE, (base_x + WIDTH, HEIGHT - BASE.get_height()))

        pygame.display.update()
        clock.tick(60)

while True:
    main()
