import pygame
from constants import ACTION_JUMP, ACTION_SEARCH
from entities.npc.flyweight import NPCFlyweightFactory
from entities.npc.npc import NPC
from entities.player.hazel import Hazel
from entities.projectile.flyweight import ProjectileFlyweightFactory
from entities.projectile.manager import ProjectileManager
from entities.projectile.weapon import Weapon
from scenes.base import Scene
from settings import (
    BACKGROUND_COLOR,
    KEY_BINDINGS,
    NPC_COLOR,
    NPC_JUMP_SPEED,
    NPC_SEARCH_RANGE,
    NPC_SIZE,
    NPC_SPEED,
    PLATFORM_COLOR,
    PLAYER_COLOR,
    PROJECTILE_COLOR,
    PROJECTILE_COOLDOWN,
    PROJECTILE_LIFETIME,
    PROJECTILE_POOL_SIZE,
    PROJECTILE_RADIUS,
    PROJECTILE_SPEED,
    TEXT_COLOR,
    WINDOW_SIZE,
)
from system.camera import Camera
from system.input_handler import InputHandler
from system.pathfinding import PlatformNavGraph
from world.level import Level


class LevelScene(Scene):
    def __init__(self):
        self.level = Level()
        self.nav_graph = PlatformNavGraph(self.level.platforms, NPC_SIZE)
        self.npc_factory = NPCFlyweightFactory([
            {
                "size": NPC_SIZE,
                "speed": NPC_SPEED,
                "jump_speed": NPC_JUMP_SPEED,
                "search_range": NPC_SEARCH_RANGE,
                "color": NPC_COLOR,
            }
        ])
        self.projectile_flyweight = ProjectileFlyweightFactory().get_flyweight({
            "radius": PROJECTILE_RADIUS,
            "speed": PROJECTILE_SPEED,
            "lifetime": PROJECTILE_LIFETIME,
            "cooldown": PROJECTILE_COOLDOWN,
            "color": PROJECTILE_COLOR,
        })
        self.projectile_manager = ProjectileManager(PROJECTILE_POOL_SIZE)
        self.camera = Camera(WINDOW_SIZE, self.level.bounds)
        self.input_handler = InputHandler()
        self.font = pygame.font.Font(None, 26)
        labels = {
            action: "/".join(pygame.key.name(key) for key in keys) or "-"
            for action, keys in KEY_BINDINGS.items()
        }
        self.help_text = self.font.render(
            f"{labels['move_left']}, {labels['move_right']}: move | "
            f"{labels[ACTION_JUMP]}: jump | {labels['shoot']}/mouse1: shoot |{labels[ACTION_SEARCH]}: npc search | "
            f"{labels['pause']}: pause | {labels['restart']}: restart | "
            f"{labels['quit']}: quit",
            True,
            TEXT_COLOR,
        )
        self.pause_text = self.font.render(
            f"Paused - press {labels['pause']} to resume", True, TEXT_COLOR
        )
        self.reset()

    def reset(self):
        self.projectile_manager.clear()
        weapon = Weapon(self.projectile_flyweight, self.projectile_manager)
        self.player = Hazel(self.level.spawn, weapon)
        stalker_flyweight = self.npc_factory.get_flyweight({
            "size": NPC_SIZE,
            "speed": NPC_SPEED,
            "jump_speed": NPC_JUMP_SPEED,
            "search_range": NPC_SEARCH_RANGE,
            "color": NPC_COLOR,
        })
        self.npcs = [
            NPC(
                spawn=self.level.npc_spawn,
                flyweight=stalker_flyweight,
                nav_graph=self.nav_graph,
                target=self.player,
            )
        ]
        self.input_handler.clear()
        self.paused = False
        self.camera.follow(self.player.rect)

    def handle_event(self, event):
        if event.type == pygame.WINDOWFOCUSLOST:
            self.paused = True
            self.input_handler.clear()
        elif event.type == pygame.KEYDOWN:
            if event.key in KEY_BINDINGS["pause"]:
                self.paused = not self.paused
                self.input_handler.clear()
            elif event.key in KEY_BINDINGS["restart"]:
                self.reset()
            elif not self.paused:
                if event.key in KEY_BINDINGS[ACTION_SEARCH]:
                    for npc in self.npcs:
                        npc.start_search()
                else:
                    self.input_handler.handle_event(event)

    def update(self, dt):
        if self.paused:
            return
        for command in self.input_handler.get_commands():
            command.execute(self.player)
        self.player.update(dt, self.level.platforms)
        self.projectile_manager.update(dt, self.level.bounds)
        for npc in self.npcs:
            npc.update(dt, self.level.platforms)
            if npc.rect.top > self.level.bounds.bottom:
                npc.position.update(npc.spawn_position)
                npc.rect.topleft = (round(npc.position.x), round(npc.position.y))
                npc.velocity.update(0, 0)
        if self.player.rect.top > self.level.bounds.bottom:
            self.reset()
        self.camera.follow(self.player.rect)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(BACKGROUND_COLOR)
        for platform in self.level.get_platforms():
            pygame.draw.rect(surface, PLATFORM_COLOR, self.camera.apply(platform))
        for npc in self.npcs:
            pygame.draw.rect(surface, npc.flyweight.color, self.camera.apply(npc.rect))
        for projectile in self.projectile_manager.active():
            pygame.draw.circle(surface, projectile.flyweight.color, self.camera.apply(projectile.rect).center, projectile.flyweight.radius)
        pygame.draw.rect(surface, PLAYER_COLOR, self.camera.apply(self.player.rect))
        # HUD coordinates stay on screen instead of passing through the camera.
        surface.blit(self.help_text, (16, 16))
        if self.paused:
            surface.blit(self.pause_text, (16, 48))
