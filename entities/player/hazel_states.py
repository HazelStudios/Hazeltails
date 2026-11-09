from constants import (
    ACTION_FALL,
    ACTION_JUMP,
    ACTION_LAND,
    ACTION_MOVE,
    ACTION_STOP,
    ANIMATION_DEAD,
    ANIMATION_FALL,
    ANIMATION_IDLE,
    ANIMATION_JUMP,
    ANIMATION_WALK,
)
from settings import JUMP_SPEED, PLAYER_SPEED
from system.fsm import State


class IdleState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.velocity.x = 0
        actor.set_animation(ANIMATION_IDLE)

    def handle_command(self, actor, command, value=None):
        if command == ACTION_MOVE and value:
            actor.velocity.x = value * PLAYER_SPEED
            return actor.walk_state
        if command == ACTION_JUMP and actor.on_ground:
            actor.velocity.y = -JUMP_SPEED
            actor.on_ground = False
            return actor.jump_state
        return None

    def update(self, actor, dt):
        if not actor.on_ground:
            actor.fsm.trigger(ACTION_FALL, actor)


class WalkState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.set_animation(ANIMATION_WALK)

    def handle_command(self, actor, command, value=None):
        if command == ACTION_MOVE and value:
            actor.velocity.x = value * PLAYER_SPEED
        elif command == ACTION_STOP:
            actor.velocity.x = 0
            return actor.idle_state
        elif command == ACTION_JUMP and actor.on_ground:
            actor.velocity.y = -JUMP_SPEED
            actor.on_ground = False
            return actor.jump_state
        return None

    def update(self, actor, dt):
        if not actor.on_ground:
            actor.fsm.trigger(ACTION_FALL, actor)


class JumpState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.set_animation(ANIMATION_JUMP)

    def handle_command(self, actor, command, value=None):
        if command == ACTION_MOVE and value:
            actor.velocity.x = value * PLAYER_SPEED
        elif command == ACTION_STOP:
            actor.velocity.x = 0
        return None

    def update(self, actor, dt):
        if actor.velocity.y >= 0:
            actor.fsm.trigger(ACTION_FALL, actor)


class FallState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.set_animation(ANIMATION_FALL)

    def handle_command(self, actor, command, value=None):
        if command == ACTION_MOVE and value:
            actor.velocity.x = value * PLAYER_SPEED
        elif command == ACTION_STOP:
            actor.velocity.x = 0
        return None

    def update(self, actor, dt):
        if actor.on_ground:
            actor.fsm.trigger(ACTION_LAND, actor)


class DeadState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.velocity.x = 0
        actor.velocity.y = 0
        actor.set_animation(ANIMATION_DEAD)

    def update(self, actor, dt: float) -> None:
        pass