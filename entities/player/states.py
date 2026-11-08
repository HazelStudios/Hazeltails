from system.fsm import State

class IdleState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.velocity.x = 0
        actor.set_animation("idle")

    def update(self, actor, dt):
        if not actor.on_ground:
            actor.fsm.trigger("fall", actor)

class WalkState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.set_animation("walk")

    def update(self, actor, dt):
        if not actor.on_ground:
            actor.fsm.trigger("fall", actor)

class JumpState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.set_animation("jump")

    def update(self, actor, dt):
        # velocity.y >= 0 -> falling down state
        if actor.velocity.y >= 0:
            actor.fsm.trigger("fall", actor)

class FallState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.set_animation("fall")

    def update(self, actor, dt):
        if actor.on_ground:
            if abs(actor.velocity.x) > 0.1: # player moving horizontally -> walk state
                actor.fsm.trigger("move", actor)
            else:
                actor.fsm.trigger("land", actor)

class DeadState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.velocity.x = 0
        actor.velocity.y = 0
        actor.set_animation("die")

    def update(self, actor, dt):
        pass