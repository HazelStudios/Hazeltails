import pygame

from entities.projectile.flyweight import ProjectileFlyweight


class Projectile:

    def __init__(self):
        self.flyweight: ProjectileFlyweight | None = None
        self.position = pygame.Vector2()
        self.velocity = pygame.Vector2()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.age = 0.0
        self.active = False

    def activate(self, flyweight, center, direction):
        self.flyweight = flyweight
        self.position.update(center)
        self.velocity.update(direction * flyweight.speed, 0)
        size = flyweight.radius * 2
        self.rect.size = (size, size)
        self.rect.center = (round(center[0]), round(center[1]))
        self.age = 0.0
        self.active = True

    def update(self, dt, bounds):
        self.position += self.velocity * dt
        self.rect.center = (round(self.position.x), round(self.position.y))
        self.age += dt
        if self.age >= self.flyweight.lifetime or not bounds.colliderect(self.rect):
            self.active = False
