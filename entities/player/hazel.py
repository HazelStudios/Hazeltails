import pygame

from settings import (
    GRAVITY,
    JUMP_SPEED,
    MAX_FALL_SPEED,
    PLAYER_SIZE,
    PLAYER_SPEED,
)
from system.fsm import FSM
from entities.player.states import IdleState, WalkState, JumpState, FallState, DeadState


class Hazel:
    """Player movement and collisions, independent of keyboard and camera"""

    def __init__(self, spawn: tuple[int, int]):
        self.position = pygame.Vector2(spawn)
        self.velocity = pygame.Vector2()
        self.rect = pygame.Rect(spawn, PLAYER_SIZE)
        self.on_ground = False
        self.current_animation = "idle"

        self.idle_state = IdleState()
        self.walk_state = WalkState()
        self.jump_state = JumpState()
        self.fall_state = FallState()
        self.dead_state = DeadState()

        self.fsm = FSM(self.idle_state, actor=self)
        self._setup_transitions()

    def _setup_transitions(self):
        t = self.fsm.add_transition
        t(self.idle_state, "move", self.walk_state)
        t(self.idle_state, "jump", self.jump_state)
        t(self.idle_state, "fall", self.fall_state)
        t(self.idle_state, "die",  self.dead_state)
        t(self.walk_state, "stop", self.idle_state)
        t(self.walk_state, "jump", self.jump_state)
        t(self.walk_state, "fall", self.fall_state)
        t(self.walk_state, "die",  self.dead_state)
        t(self.jump_state, "fall", self.fall_state)
        t(self.jump_state, "die",  self.dead_state)
        t(self.fall_state, "land", self.idle_state)
        t(self.fall_state, "move", self.walk_state)
        t(self.fall_state, "die",  self.dead_state)

    def set_animation(self, anim_name):
        self.current_animation = anim_name

    def move(self, direction):
        if self.fsm.current is self.dead_state:
            return
        self.velocity.x = direction * PLAYER_SPEED
        if direction != 0:
            if self.on_ground:
                self.fsm.trigger("move", self)
        else:
            if self.on_ground:
                self.fsm.trigger("stop", self)

    def jump(self):
        if self.fsm.current is self.dead_state:
            return
        if self.on_ground:
            self.velocity.y = -JUMP_SPEED
            self.on_ground = False
            self.fsm.trigger("jump", self)

    def update(self, dt, platforms):
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