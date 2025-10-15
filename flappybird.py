import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Floppy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Game variables
FPS = 60
clock = pygame.time.Clock()
game_over = False
score = 0
font = pygame.font.Font(None, 50)

# Bird properties
bird_width = 40
bird_height = 30
bird_x = 50
bird_y = SCREEN_HEIGHT // 2 - bird_height // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -7

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_speed = 3
pipes = []

# Background
try:
    background_img = pygame.image.load('background.jfif ').convert()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print("Error loading background image. Using a solid blue background.")
    background_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_img.fill(BLUE)

# Bird image
try:
    bird_img = pygame.image.load('bird.png').convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))
except pygame.error:
    print("Error loading bird image. Using a solid green rectangle for the bird.")
    bird_img = pygame.Surface((bird_width, bird_height))
    bird_img.fill(GREEN)

# Function to draw bird
def draw_bird(x, y):
    screen.blit(bird_img, (x, y))

# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe[0]) # Top pipe
        pygame.draw.rect(screen, GREEN, pipe[1]) # Bottom pipe

# Function to create new pipes
def create_pipe():
    pipe_height = random.randint(150, SCREEN_HEIGHT - pipe_gap - 150)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_height - pipe_gap)
    return top_pipe, bottom_pipe

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Function to display game over message
def game_over_screen(score):
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Press SPACE to Restart", True, BLACK)

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)

# Game loop
def main():
    global bird_y, bird_velocity, game_over, score, pipes

    # Reset game state
    bird_y = SCREEN_HEIGHT // 2 - bird_height // 2
    bird_velocity = 0
    game_over = False
    score = 0
    pipes = []
    pipes.append(create_pipe()) # Initial pipe

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        bird_velocity = jump_strength
                    else:
                        main() # Restart game

        if not game_over:
            # Bird movement
            bird_velocity += gravity
            bird_y += bird_velocity

            # Pipe movement
            for pipe in pipes:
                pipe[0].x -= pipe_speed
                pipe[1].x -= pipe_speed

            # Add new pipes
            if pipes[-1][0].x < SCREEN_WIDTH - 200: # Create new pipe when last one is sufficiently far
                pipes.append(create_pipe())

            # Remove off-screen pipes and update score
            for pipe in pipes[:]:
                if pipe[0].right < 0:
                    pipes.remove(pipe)
                if pipe[0].left < bird_x and pipe[0].right > bird_x and not game_over:
                    if bird_x > pipe[0].centerx - pipe_speed and bird_x < pipe[0].centerx: # Check if bird passed the pipe
                        score += 1

            # Collision detection
            bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
            if bird_y > SCREEN_HEIGHT - bird_height or bird_y < 0: # Ground or ceiling collision
                game_over = True
            for pipe in pipes:
                if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
                    game_over = True

        # Drawing
        screen.blit(background_img, (0, 0))
        draw_pipes(pipes)
        draw_bird(bird_x, bird_y)
        display_score(score)

        if game_over:
            game_over_screen(score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()