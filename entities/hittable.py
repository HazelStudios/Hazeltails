from settings import HIT_FLASH_DURATION


class Hittable:
    """Entities that projectiles can hit"""
    hit_flash_timer = 0.0

    def on_hit(self, projectile):
        self.hit_flash_timer = HIT_FLASH_DURATION

    def update_hit_flash(self, dt):
        self.hit_flash_timer = max(0.0, self.hit_flash_timer - dt)
