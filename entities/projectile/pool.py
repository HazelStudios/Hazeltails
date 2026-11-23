import pygame

from entities.projectile.flyweight import ProjectileFlyweight
from entities.projectile.projectile import Projectile


class ProjectilePool:
    """Fixed set of reusable projectiles"""

    def __init__(self, size: int):
        self._projectiles = [Projectile() for _ in range(size)]

    def spawn(self, flyweight, owner, center, direction):
        for projectile in self._projectiles:
            if not projectile.active:
                projectile.activate(flyweight, owner, center, direction)
                return

    def active(self):
        return (p for p in self._projectiles if p.active)

    def clear(self):
        for projectile in self._projectiles:
            projectile.active = False
