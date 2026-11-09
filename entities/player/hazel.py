import pygame

from constants import (
    ACTION_DIE,
    ACTION_FALL,
    ACTION_JUMP,
    ACTION_LAND,
    ACTION_MOVE,
    ACTION_STOP,
    ANIMATION_IDLE,
)
from settings import (
    GRAVITY,
    MAX_FALL_SPEED,
    PLAYER_SIZE,
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
        (idle_state, ACTION_MOVE): walk_state,
        (idle_state, ACTION_JUMP): jump_state,
        (idle_state, ACTION_FALL): fall_state,
        (idle_state, ACTION_DIE): dead_state,
        # Walk transitions
        (walk_state, ACTION_STOP): idle_state,
        (walk_state, ACTION_JUMP): jump_state,
        (walk_state, ACTION_FALL): fall_state,
        (walk_state, ACTION_DIE): dead_state,
        # Jump transitions
        (jump_state, ACTION_FALL): fall_state,
        (jump_state, ACTION_LAND): idle_state,
        (jump_state, ACTION_MOVE): walk_state,
        (jump_state, ACTION_DIE): dead_state,
        # Fall transitions
        (fall_state, ACTION_LAND): idle_state,
        (fall_state, ACTION_MOVE): walk_state,
        (fall_state, ACTION_DIE): dead_state,
    }

    def __init__(self, spawn: tuple[int, int]):
        self.position = pygame.Vector2(spawn)
        self.velocity = pygame.Vector2()
        self.rect = pygame.Rect(spawn, PLAYER_SIZE)
        self.on_ground = False
        self.current_animation = ANIMATION_IDLE
        self.fsm = FSM(self.idle_state, transitions=self.transitions, actor=self)

    def set_animation(self, anim_name: str) -> None:
        """Update current animation identifier for renderer integration."""
        self.current_animation = anim_name

    def move(self, direction: int) -> None:
        """Forward movement to the current state."""
        action = ACTION_MOVE if direction != 0 else ACTION_STOP
        self.fsm.handle_command(self, action, direction)

    def jump(self) -> None:
        """Forward the jump action to the current state."""
        self.fsm.handle_command(self, ACTION_JUMP)

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