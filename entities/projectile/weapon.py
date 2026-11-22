from entities.projectile.flyweight import ProjectileFlyweight
from entities.projectile.manager import ProjectileManager


class Weapon:
    """Fires one kind of projectile with a cooldown"""

    def __init__(self, flyweight: ProjectileFlyweight, manager: ProjectileManager):
        self.flyweight = flyweight
        self.manager = manager
        self.cooldown_timer = 0.0

    def update(self, dt):
        self.cooldown_timer = max(0.0, self.cooldown_timer - dt)

    def fire(self, origin, direction) -> None:
        if self.cooldown_timer > 0:
            return
        self.cooldown_timer = self.flyweight.cooldown
        self.manager.spawn(self.flyweight, origin, direction)
