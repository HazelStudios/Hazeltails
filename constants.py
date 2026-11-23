from typing import Final

# Actions that can be handled by Hazel's state machine.
ACTION_MOVE: Final = "move"
ACTION_STOP: Final = "stop"
ACTION_JUMP: Final = "jump"
ACTION_FALL: Final = "fall"
ACTION_LAND: Final = "land"
ACTION_DIE: Final = "die"

# Actions for NPC state machine.
ACTION_SEARCH: Final = "search"
ACTION_RETURN: Final = "return"
ACTION_IDLE: Final = "idle"

# Animation identifiers used until the animation system is implemented.
ANIMATION_IDLE: Final = "idle"
ANIMATION_WALK: Final = "walk"
ANIMATION_JUMP: Final = "jump"
ANIMATION_FALL: Final = "fall"
ANIMATION_DEAD: Final = "die"
ANIMATION_SEARCH: Final = "search"
ANIMATION_RETURN: Final = "return"