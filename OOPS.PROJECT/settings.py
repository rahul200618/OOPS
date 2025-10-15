import pygame
import os

try:
    pygame.init()
    display_info = pygame.display.Info()
    SCREEN_WIDTH = display_info.current_w
    SCREEN_HEIGHT = display_info.current_h
except pygame.error:
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080


GAME_WIDTH = 800
GAME_HEIGHT = 600

FPS = 60
TITLE = "Don't Even Bother - PURE EVIL"

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, "assets")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
DARK_RED = (80, 0, 0)
GREEN = (50, 205, 50)
DARK_GREEN = (0, 100, 0)
BLUE = (70, 130, 255)
DARK_BLUE = (10, 20, 40)
PURPLE = (138, 43, 226)
DARK_PURPLE = (25, 10, 35)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)

GRAVITY = 2500
PLAYER_SPEED = 300
JUMP_FORCE = -650
ACCELERATION = 3000
DECELERATION = 2200

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32

DEATH_MESSAGES = [
    "Did you even try?", "My grandma is better", "Just quit already", "Pathetic",
    "Are you even trying?", "LOL", "Git gud scrub", "Skill issue detected",
    "Delete the game", "Imagine dying here", "You're embarrassing",
    "Try using your hands", "Is this your first game?", "Literally how", "Yikes...",
    "Maybe try an easier game", "This is sad to watch", "Your parents are disappointed",
    "Brain not found. Respawn instead.", "Even the tutorial NPCs do better.",
    "Pro tip: Try not dying next time.", "Was that your strategy, or a cry for help?",
    "You make losing look effortless!", "Achievement unlocked: Instant Regret.",
    "Respawning... because we both know you’ll die again."
]
