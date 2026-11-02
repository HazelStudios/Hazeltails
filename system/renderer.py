import pygame

from scenes.base import Scene
from settings import TITLE, WINDOW_SIZE


class Renderer:
    """Own the display; each scene decides what to draw on it"""

    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(TITLE)

    def render(self, scene) -> None:
        scene.render(self.screen)
        pygame.display.flip()
