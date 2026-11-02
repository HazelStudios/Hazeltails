import pygame


class Camera:
    """Translate world rectangles into screen coordinates without moving them"""

    def __init__(self, window_size, bounds: pygame.Rect):
        self.window_size = window_size
        self.bounds = bounds.copy()
        self.offset = pygame.Vector2()

    def follow(self, target: pygame.Rect):
        width, height = self.window_size
        max_x = max(self.bounds.left, self.bounds.right - width)
        max_y = max(self.bounds.top, self.bounds.bottom - height)
        self.offset.x = max(self.bounds.left, min(target.centerx - width / 2, max_x))
        self.offset.y = max(self.bounds.top, min(target.centery - height / 2, max_y))

    def apply(self, rect):
        return rect.move(-round(self.offset.x), -round(self.offset.y))
