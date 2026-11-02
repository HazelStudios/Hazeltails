import pygame

from scenes.base import Scene
from scenes.level_scene import LevelScene
from settings import FIXED_DT, MAX_FRAME_TIME, TARGET_FPS
from system.renderer import Renderer


class Game:
    def __init__(self):
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
        self.scene = LevelScene()
        self.running = False

    def change_scene(self, scene: Scene) -> None:
        self.scene = scene

    def run(self):
        self.running = True
        budget = 0.0
        while self.running:
            # Bound catch-up work after a stall or window drag.
            frame_time = min(self.clock.tick(TARGET_FPS) / 1000.0, MAX_FRAME_TIME)
            self.handle_events()
            if not self.running:
                break

            budget += frame_time
            while budget >= FIXED_DT:
                self.update(FIXED_DT)
                budget -= FIXED_DT
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                return
            self.scene.handle_event(event)

    def update(self, dt):
        self.scene.update(dt)

    def render(self):
        self.renderer.render(self.scene)
