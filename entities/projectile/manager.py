import pygame

from entities.projectile.pool import ProjectilePool


class ProjectileManager:
    """Owns one pool per flyweight, so new projectile types need no extra code"""

    def __init__(self, pool_size: int):
        self._pool_size = pool_size
        self._pools = {}

    def spawn(self, flyweight, center, direction):
        if flyweight not in self._pools:
            self._pools[flyweight] = ProjectilePool(self._pool_size)
        self._pools[flyweight].spawn(flyweight, center, direction)

    def update(self, dt, bounds: pygame.Rect):
        for pool in self._pools.values():
            pool.update(dt, bounds)

    def active(self):
        for pool in self._pools.values():
            yield from pool.active()

    def clear(self):
        for pool in self._pools.values():
            pool.clear()
