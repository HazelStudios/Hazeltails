import pygame


class Level:
    """Temporary level geometry"""

    def __init__(self):
        self.bounds = pygame.Rect(0, 0, 2200, 720)
        self.spawn = (80, 400)
        self.platforms = [
            pygame.Rect(0, 500, 800, 220),
            pygame.Rect(940, 500, 1260, 220),
            pygame.Rect(280, 400, 160, 24),
            pygame.Rect(540, 310, 160, 24),
            pygame.Rect(1040, 390, 180, 24),
            pygame.Rect(1360, 300, 180, 24),
            pygame.Rect(1690, 390, 180, 24),
            pygame.Rect(-32, 0, 32, 720),
            pygame.Rect(2200, 0, 32, 720),
        ]

    def get_platforms(self):
        return self.platforms
