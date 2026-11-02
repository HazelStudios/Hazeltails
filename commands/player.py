from abc import ABC, abstractmethod
from dataclasses import dataclass

from entities.player.hazel import Hazel


class Command(ABC):
    @abstractmethod
    def execute(self, player: Hazel):
        pass


@dataclass(frozen=True)
class LeftCommand(Command):
    def execute(self, player: Hazel) -> None:
        player.move(-1)

@dataclass(frozen=True)
class RightCommand(Command):
    def execute(self, player: Hazel) -> None:
        player.move(1)


class StopCommand(Command):
    def execute(self, player: Hazel) -> None:
        player.move(0)


class JumpCommand(Command):
    def execute(self, player: Hazel) -> None:
        player.jump()
