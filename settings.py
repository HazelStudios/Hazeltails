from pathlib import Path
import pygame

from constants import ACTION_JUMP

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"

TITLE = "Hazeltails"
WINDOW_SIZE = (960, 540)
TARGET_FPS = 60
FIXED_DT = 1.0 / 120.0
MAX_FRAME_TIME = 0.1

# Distances in pixels; speeds in pixels/second; gravity in pixels/second².
PLAYER_SIZE = (32, 48)
PLAYER_SPEED = 250.0
JUMP_SPEED = 800.0
GRAVITY = 1800.0
MAX_FALL_SPEED = 900.0

BACKGROUND_COLOR = (26, 32, 44)
PLATFORM_COLOR = (82, 125, 90)
PLAYER_COLOR = (225, 157, 88)
TEXT_COLOR = (235, 235, 235)

KEY_BINDINGS = {
    "move_left": [pygame.K_a, pygame.K_LEFT],
    "move_right": [pygame.K_d, pygame.K_RIGHT],
    ACTION_JUMP: [pygame.K_SPACE],
    "pause": [pygame.K_p],
    "restart": [pygame.K_r],
    "quit": [pygame.K_ESCAPE],
}
