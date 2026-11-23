import pygame
from constants import ACTION_SEARCH, ANIMATION_IDLE
from entities.hittable import Hittable
from entities.npc.flyweight import NPCFlyweight
from settings import GRAVITY, MAX_FALL_SPEED
from system.fsm import FSM
from system.pathfinding import PlatformNavGraph


class NPC(Hittable):

    def __init__(
        self,
        spawn: tuple[int, int],
        flyweight: NPCFlyweight,
        nav_graph: PlatformNavGraph,
        target,
    ):
        self.flyweight = flyweight
        self.nav_graph = nav_graph
        self.target = target

        self.spawn = spawn
        self.position = pygame.Vector2(spawn)
        self.velocity = pygame.Vector2()
        self.rect = pygame.Rect(spawn, self.flyweight.size)
        self.on_ground = False
        self.current_animation = ANIMATION_IDLE

        # External A* pathfinding data
        self.path: list[tuple[pygame.Vector2, str]] = []
        self.repath_timer: float = 0.0

        self.fsm = FSM(
            self.flyweight.idle_state,
            transitions=self.flyweight.transitions,
            actor=self,
        )

    def set_animation(self, anim_name):
        """Update current animation identifier for renderer integration."""
        self.current_animation = anim_name

    def start_search(self):
        """Forward the search action to the current state."""
        self.fsm.handle_command(self, ACTION_SEARCH)

    def update(self, dt, platforms: list[pygame.Rect]):
        """Advance physics simulation, resolve collisions per axis, and synchronize state machine."""
        self.update_hit_flash(dt)
        self.velocity.y = min(self.velocity.y + GRAVITY * dt, MAX_FALL_SPEED)

        # Resolve each axis separately so touching a wall does not stop a fall
        self.position.x += self.velocity.x * dt
        self.rect.x = round(self.position.x)
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.x > 0:
                    self.rect.right = platform.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.right
                else:
                    continue
                self.position.x = self.rect.x
                self.velocity.x = 0

        self.position.y += self.velocity.y * dt
        self.rect.y = round(self.position.y)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.bottom
                else:
                    continue
                self.position.y = self.rect.y
                self.velocity.y = 0

        # Rect uses integers: a tiny downward step may not overlap the floor yet
        if self.velocity.y >= 0:
            self.on_ground = any(
                self.rect.bottom == platform.top
                and self.rect.left < platform.right
                and self.rect.right > platform.left
                for platform in platforms
            )

        # Update the FSM after physics to ensure the state reflects the current situation
        self.fsm.update(self, dt)
