import pygame

from entities.player.hazel import Hazel
from scenes.base import Scene
from settings import (
    BACKGROUND_COLOR,
    PLATFORM_COLOR,
    PLAYER_COLOR,
    TEXT_COLOR,
    WINDOW_SIZE,
)
from system.camera import Camera
from system.input_handler import InputHandler
from world.level import Level


class LevelScene(Scene):
    def __init__(self):
        self.level = Level()
        self.camera = Camera(WINDOW_SIZE, self.level.bounds)
        self.input_handler = InputHandler()
        self.font = pygame.font.Font(None, 26)
        self.help_text = self.font.render("A/D or arrows: move | Space: jump | P: pause | R: restart | Esc: quit", True, TEXT_COLOR)
        self.pause_text = self.font.render("Paused - press P to resume", True, TEXT_COLOR)
        self.reset()

    def reset(self):
        self.player = Hazel(self.level.spawn)
        self.input_handler.clear()
        self.paused = False
        self.camera.follow(self.player.rect)

    def handle_event(self, event):
        if event.type == pygame.WINDOWFOCUSLOST:
            self.paused = True
            self.input_handler.clear()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.paused = not self.paused
                self.input_handler.clear()
            elif event.key == pygame.K_r:
                self.reset()
            elif not self.paused:
                self.input_handler.handle_event(event)

    def update(self, dt):
        if self.paused:
            return
        for command in self.input_handler.get_commands():
            command.execute(self.player)
        self.player.update(dt, self.level.platforms)
        if self.player.rect.top > self.level.bounds.bottom:
            self.reset()
        self.camera.follow(self.player.rect)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)
        for platform in self.level.get_platforms():
            pygame.draw.rect(surface, PLATFORM_COLOR, self.camera.apply(platform))
        pygame.draw.rect(surface, PLAYER_COLOR, self.camera.apply(self.player.rect))
        # HUD coordinates stay on screen instead of passing through the camera.
        surface.blit(self.help_text, (16, 16))
        if self.paused:
            surface.blit(self.pause_text, (16, 48))
