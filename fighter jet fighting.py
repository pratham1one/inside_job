import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("fighter jet")

# Set up assets
player_img = pygame.image.load("player.png.png")
player_img = pygame.transform.scale(player_img, (60, 60))

enemy_img = pygame.image.load("enemy.png.png")
enemy_img = pygame.transform.rotate(enemy_img, 180)  # Rotate 180 degrees

# Load images
player_img = pygame.image.load("player.png.png")
enemy_img = pygame.image.load("enemy.png.png")


# Resize images
player_size = 60
enemy_size = 60
player_img = pygame.transform.scale(player_img, (60,60))
enemy_img = pygame.transform.scale(enemy_img, (80,80))

#Rotate enemy to face downward
enemy_img = pygame.transform.rotate(enemy_img, 180)

bullet_img = pygame.Surface((5, 10))
bullet_img.fill((255, 0, 0))

background_img = pygame.image.load("background.img.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

heart_img = pygame.image.load("heart.png")
heart_img = pygame.transform.scale(heart_img, (30, 30))

explosion_img = pygame.image.load("explosion.jpg")
explosion_img = pygame.transform.scale(background_img, (30, 30))

# load sound
shoot_sound = pygame.mixer.Sound("laser sound.mp3")
explosion_sound = pygame.mixer.Sound("explosion.mp3")

# Game variables
player_x = WIDTH // 2
player_y = HEIGHT - 70
player_velocity = 5

bullets = []
bullet_velocity = 7

enemy_x = random.randint(0, WIDTH - 60)
enemy_y = -60
enemy_velocity = 2

score = 0
high_score = 0
lives = 5
speed_increased_at = 0

# Load high score if available
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())

# Fonts
font = pygame.font.SysFont(None, 36)

# Clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    clock.tick(60)
    screen.blit(background_img, (0, 0))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 60:
        player_x += player_velocity
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:
            bullets.append([player_x + 28, player_y])

    # Update Bullets
    for bullet in bullets:
        bullet[1] -= bullet_velocity
    bullets = [b for b in bullets if b[1] > -10]

    # Update Enemy
    enemy_y += enemy_velocity

    if enemy_y > HEIGHT:
        enemy_x = random.randint(0, WIDTH - 60)
        enemy_y = -60
        lives -= 1
        if score - speed_increased_at >= 100:
            enemy_velocity += 0.3
            if enemy_velocity > 10:
                enemy_velocity = 10
            speed_increased_at = score

    # Collision Detection
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 60, 60)
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
        if bullet_rect.colliderect(enemy_rect):
            bullets.remove(bullet)
            score += 10
            enemy_x = random.randint(0, WIDTH - 60)
            enemy_y = -60
            if score - speed_increased_at >= 100:
                enemy_velocity += 0.3
                if enemy_velocity > 10:
                    enemy_velocity = 10
                speed_increased_at = score
            break

    # Draw Player
    screen.blit(player_img, (player_x, player_y))

    # Draw Bullets
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

    # Draw Enemy
    screen.blit(enemy_img, (enemy_x, enemy_y))

    # Draw Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw High Score
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    screen.blit(high_score_text, (350, 10))

    # Draw Lives (hearts)
    for i in range(lives):
        screen.blit(heart_img, (10 + i * 35, 50))

    # Game Over
    if lives <= 0:
        game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

# Save high score
if score > high_score:
    with open("highscore.txt", "w") as f:
        f.write(str(score))

pygame.quit()

