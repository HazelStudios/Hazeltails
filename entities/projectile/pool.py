import pygame

from entities.projectile.flyweight import ProjectileFlyweight
from entities.projectile.projectile import Projectile


class ProjectilePool:
    """Fixed set of reusable projectiles"""

    def __init__(self, size: int):
        self._projectiles = [Projectile() for _ in range(size)]

    def spawn(self, flyweight, center, direction):
        for projectile in self._projectiles:
            if not projectile.active:
                projectile.activate(flyweight, center, direction)
                return

    def update(self, dt, bounds):
        for projectile in self._projectiles:
            if projectile.active:
                projectile.update(dt, bounds)

    def active(self):
        return (p for p in self._projectiles if p.active)

    def clear(self):
        for projectile in self._projectiles:
            projectile.active = False
