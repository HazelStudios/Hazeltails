import pygame

from settings import (
    GRAVITY,
    JUMP_SPEED,
    MAX_FALL_SPEED,
    PLAYER_SIZE,
    PLAYER_SPEED,
)


class Hazel:
    """Player movement and collisions, independent of keyboard and camera"""

    def __init__(self, spawn: tuple[int, int]):
        self.position = pygame.Vector2(spawn)
        self.velocity = pygame.Vector2()
        self.rect = pygame.Rect(spawn, PLAYER_SIZE)
        self.on_ground = False

    def move(self, direction):
        self.velocity.x = direction * PLAYER_SPEED

    def jump(self):
        if self.on_ground:
            self.velocity.y = -JUMP_SPEED
            self.on_ground = False

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
