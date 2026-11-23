import pygame

from entities.projectile.pool import ProjectilePool
from system.spatial_grid import SpatialGrid


class ProjectileManager:
    """Owns one pool per flyweight and resolves projectile collisions"""

    def __init__(self, pool_size: int, cell_size: int):
        self.pool_size = pool_size
        self.pools = {}
        self.obstacles = SpatialGrid(cell_size) # Static obstacles
        self.targets = SpatialGrid(cell_size) # Dynamic targets, like players and enemies

    def set_obstacles(self, obstacles: list[pygame.Rect]):
        self.obstacles.clear()
        for rect in obstacles:
            self.obstacles.insert(rect, rect)

    def spawn(self, flyweight, owner, center, direction):
        if flyweight not in self.pools:
            self.pools[flyweight] = ProjectilePool(self.pool_size)
        self.pools[flyweight].spawn(flyweight, owner, center, direction)

    def update(self, dt, bounds, targets):
        # Targets move, so their grid is rebuilt every step
        self.targets.clear()
        for target in targets:
            self.targets.insert(target, target.rect)

        for projectile in self.active():
            projectile.update(dt, bounds)
            if projectile.active:
                self.check_collisions(projectile)

    def check_collisions(self, projectile):
        rect = projectile.rect
        for target in self.targets.query(rect):
            if target is not projectile.owner and rect.colliderect(target.rect):
                target.on_hit(projectile)
                projectile.active = False
                return
        for obstacle in self.obstacles.query(rect):
            if rect.colliderect(obstacle):
                projectile.active = False
                return

    def active(self):
        for pool in self.pools.values():
            yield from pool.active()

    def clear(self):
        for pool in self.pools.values():
            pool.clear()
