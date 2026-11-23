import pygame

from commands.player import Command, JumpCommand, LeftCommand, RightCommand, ShootCommand, StopCommand
from settings import KEY_BINDINGS


class InputHandler:
    """Translate keyboard input into commands without knowing the player"""

    def __init__(self):
        self._pending_commands: list[Command] = []
        self._jump_command = JumpCommand()
        self._shoot_command = ShootCommand()
        self._movement_commands = {
            -1: LeftCommand(),
            0: StopCommand(),
            1: RightCommand(),
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in KEY_BINDINGS["jump"]:
            self._pending_commands.append(self._jump_command)

    def get_commands(self) -> list[Command]:
        """Sample movement each step and consume queued actions exactly once"""
        keys = pygame.key.get_pressed()
        right = any(keys[key] for key in KEY_BINDINGS["move_right"])
        left = any(keys[key] for key in KEY_BINDINGS["move_left"])
        direction = int(right) - int(left)
        commands = [self._movement_commands[direction], *self._pending_commands]
        # Holding the button keeps the command (with the cooldown), also fires on mouse 1
        if any(keys[key] for key in KEY_BINDINGS["shoot"]) or pygame.mouse.get_pressed()[0]:
            commands.append(self._shoot_command)
        self.clear()
        return commands

    def clear(self):
        self._pending_commands.clear()
