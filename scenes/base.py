from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    """Small contract shared by gameplay, future menus and other screens"""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        pass
