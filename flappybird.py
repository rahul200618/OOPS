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
gravity = 0.4
jump_strength = -6

# Pipe properties
pipe_width = 70
pipe_gap = 170
pipe_speed = 3
pipes = []

# Level variables
current_level = 1
level_up_score = 5 # Score needed to advance to the next level

# Background
try:
    background_img = pygame.image.load('background.jpg').convert()
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

# Pipe images (loaded once)
pipe_top_img_loaded = None
pipe_bottom_img_loaded = None
try:
    pipe_top_img_loaded = pygame.image.load('top.png').convert_alpha()
    pipe_bottom_img_loaded = pygame.image.load('bottom.png').convert_alpha()
except pygame.error:
    print("Error loading pipe images. Using solid green rectangles for pipes.") # This line was already present, no change needed.

# Function to draw bird
def draw_bird(x, y):
    screen.blit(bird_img, (x, y))

# Function to draw pipes
def draw_pipes(pipes):
    # Use the globally loaded pipe images
    for pipe_data in pipes:
        top_rect = pipe_data['top_rect']
        bottom_rect = pipe_data['bottom_rect']

        if pipe_top_img_loaded:
            scaled_top_img = pygame.transform.scale(pipe_top_img_loaded, (top_rect.width, top_rect.height))
            screen.blit(scaled_top_img, top_rect)
        else:
            pygame.draw.rect(screen, GREEN, top_rect) # Top pipe fallback
        if pipe_bottom_img_loaded:
            scaled_bottom_img = pygame.transform.scale(pipe_bottom_img_loaded, (bottom_rect.width, bottom_rect.height))
            screen.blit(scaled_bottom_img, bottom_rect)
        else:
            pygame.draw.rect(screen, GREEN, bottom_rect) # Bottom pipe fallback

# Function to create new pipes
def create_pipe(level):
    # Adjust pipe generation based on level
    min_height = 100
    max_height = SCREEN_HEIGHT - pipe_gap - 100

    if level == 1: # Easy
        pipe_height = random.randint(int(SCREEN_HEIGHT * 0.3), int(SCREEN_HEIGHT * 0.7) - pipe_gap)
        current_pipe_gap = pipe_gap
    elif level == 2: # Medium
        pipe_height = random.randint(int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.8) - pipe_gap)
        current_pipe_gap = pipe_gap - 20 # Slightly smaller gap
    elif level == 3: # Hard
        pipe_height = random.randint(int(SCREEN_HEIGHT * 0.1), int(SCREEN_HEIGHT * 0.9) - pipe_gap)
        current_pipe_gap = pipe_gap - 40 # Even smaller gap
    else: # Very Hard (or beyond)
        pipe_height = random.randint(min_height, max_height - pipe_gap)
        current_pipe_gap = pipe_gap - 60 # Smallest gap

    # Ensure pipe height is within bounds after adjustments
    pipe_height = max(min_height, min(pipe_height, max_height - current_pipe_gap))

    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + current_pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_height - current_pipe_gap)
    return {'top_rect': top_pipe, 'bottom_rect': bottom_pipe, 'scored': False} # Return a dictionary with a 'scored' flag

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
    global bird_y, bird_velocity, game_over, score, pipes, current_level, pipe_speed

    # Reset game state
    bird_y = SCREEN_HEIGHT // 2 - bird_height // 2
    bird_velocity = 0
    game_over = False
    score = 0
    pipes = []
    current_level = 1
    pipes.append(create_pipe(current_level)) # Initial pipe, now returns a dict

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
                pipe['top_rect'].x -= pipe_speed
                pipe['bottom_rect'].x -= pipe_speed

            # Add new pipes
            if pipes[-1]['top_rect'].x < SCREEN_WIDTH - 200: # Create new pipe when last one is sufficiently far
                pipes.append(create_pipe(current_level))

            # Remove off-screen pipes and update score
            for pipe in pipes[:]:
                if pipe['top_rect'].right < 0:
                    pipes.remove(pipe)

            # Score and level progression
            # Check if bird passed the pipe
            for pipe_data in pipes:
                if pipe_data['top_rect'].right < bird_x and not pipe_data['scored']:
                    score += 1
                    pipe_data['scored'] = True # Mark pipe as scored

            # Collision detection
            bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
            if bird_y > SCREEN_HEIGHT - bird_height or bird_y < 0: # Ground or ceiling collision
                game_over = True
            for pipe in pipes:
                if bird_rect.colliderect(pipe['top_rect']) or bird_rect.colliderect(pipe['bottom_rect']):
                    game_over = True

            # Level progression
            if score >= level_up_score * current_level:
                current_level += 1
                pipe_speed += 0.5 # Increase pipe speed for next level
                print(f"Level Up! Current Level: {current_level}, Pipe Speed: {pipe_speed}")

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