import pygame

from settings import (
    GRAVITY,
    JUMP_SPEED,
    MAX_FALL_SPEED,
    PLAYER_SIZE,
    PLAYER_SPEED,
)
from system.fsm import FSM
from entities.player.hazel_states import IdleState, WalkState, JumpState, FallState, DeadState


class Hazel:
    """Player movement and collisions, independent of keyboard and camera"""
    idle_state = IdleState()
    walk_state = WalkState()
    jump_state = JumpState()
    fall_state = FallState()
    dead_state = DeadState()

    transitions = {
        # Idle transitions
        (idle_state, "move"): walk_state,
        (idle_state, "jump"): jump_state,
        (idle_state, "fall"): fall_state,
        (idle_state, "die"): dead_state,
        # Walk transitions
        (walk_state, "stop"): idle_state,
        (walk_state, "jump"): jump_state,
        (walk_state, "fall"): fall_state,
        (walk_state, "die"): dead_state,
        # Jump transitions
        (jump_state, "fall"): fall_state,
        (jump_state, "land"): idle_state,
        (jump_state, "move"): walk_state,
        (jump_state, "die"): dead_state,
        # Fall transitions
        (fall_state, "land"): idle_state,
        (fall_state, "move"): walk_state,
        (fall_state, "die"): dead_state,
    }

    def __init__(self, spawn: tuple[int, int]):
        self.position = pygame.Vector2(spawn)
        self.velocity = pygame.Vector2()
        self.rect = pygame.Rect(spawn, PLAYER_SIZE)
        self.on_ground = False
        self.current_animation = "idle"
        self.fsm = FSM(self.idle_state, transitions=self.transitions, actor=self)

    def set_animation(self, anim_name: str) -> None:
        """Update current animation identifier for renderer integration."""
        self.current_animation = anim_name

    def move(self, direction: int) -> None:
        """Apply horizontal input direction to velocity and signal FSM."""
        if self.fsm.current is self.dead_state:
            return
        self.velocity.x = direction * PLAYER_SPEED
        if direction != 0:
            if self.on_ground:
                self.fsm.trigger("move", self)
        else:
            if self.on_ground:
                self.fsm.trigger("stop", self)

    def jump(self) -> None:
        """Apply upward impulse if grounded and signal FSM."""
        if self.fsm.current is self.dead_state:
            return
        if self.on_ground:
            self.velocity.y = -JUMP_SPEED
            self.on_ground = False
            self.fsm.trigger("jump", self)

    def update(self, dt: float, platforms: list[pygame.Rect]) -> None:
        """Advance physics simulation, resolve collisions per axis, and synchronize state machine."""
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