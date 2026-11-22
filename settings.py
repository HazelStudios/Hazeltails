from pathlib import Path
import pygame
from constants import ACTION_JUMP, ACTION_SEARCH

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"

TITLE = "Hazeltails"
WINDOW_SIZE = (960, 540)
TARGET_FPS = 60
FIXED_DT = 1.0 / 120.0
MAX_FRAME_TIME = 0.1

# Distances in pixels; speeds in pixels/second; gravity in pixels/second
PLAYER_SIZE = (32, 48)
PLAYER_SPEED = 250.0
JUMP_SPEED = 800.0
GRAVITY = 1800.0
MAX_FALL_SPEED = 900.0

# NPC Flyweight & Pathfinding settings
NPC_SIZE = (32, 48)
NPC_SPEED = 210.0
NPC_JUMP_SPEED = 800.0
NPC_SEARCH_RANGE = 3000.0
NPC_WAYPOINT_STEP = 64
NPC_REPATH_INTERVAL = 0.25

# Projectile settings
PROJECTILE_RADIUS = 6
PROJECTILE_SPEED = 600.0
PROJECTILE_LIFETIME = 1.5
PROJECTILE_COOLDOWN = 0.60
PROJECTILE_COLOR = (255, 220, 40)
PROJECTILE_POOL_SIZE = 16

BACKGROUND_COLOR = (26, 32, 44)
PLATFORM_COLOR = (82, 125, 90)
PLAYER_COLOR = (225, 157, 88)
NPC_COLOR = (214, 93, 108)
TEXT_COLOR = (235, 235, 235)

KEY_BINDINGS = {
    "move_left": [pygame.K_a, pygame.K_LEFT],
    "move_right": [pygame.K_d, pygame.K_RIGHT],
    ACTION_JUMP: [pygame.K_SPACE],
    ACTION_SEARCH: [pygame.K_m],
    "shoot": [pygame.K_k],
    "pause": [pygame.K_p],
    "restart": [pygame.K_r],
    "quit": [pygame.K_ESCAPE],
}
