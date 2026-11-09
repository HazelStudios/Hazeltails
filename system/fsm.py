from typing import Any, Optional

class State:
    def __init__(self, name: Optional[str] = None):
        self.name: str = name or self.__class__.__name__

    def enter(self, actor):
        print(f"Entering state: {self.name}")

    def handle_command(self, actor, command):
        return None

    def update(self, actor, dt):
        return None

    def exit(self, actor):
        print(f"Exiting state: {self.name}")

class FSM:
    def __init__(self, initial_state: State, transitions: Optional[dict] = None, actor = None):
        self.current = initial_state
        self.transitions = dict(transitions) if transitions is not None else {}
        if actor is not None:
            self.current.enter(actor)

    def change_state(self, next_state: Optional[State], actor):
        if next_state is not None and next_state is not self.current:
            self.current.exit(actor)
            self.current = next_state
            self.current.enter(actor)

    def add_transition(self, from_state: State, event, to_state: State):
        self.transitions[(from_state, event)] = to_state

    def trigger(self, event, actor):
        target = self.transitions.get((self.current, event))
        if target and target is not self.current:
            print(f"Transition: {self.current.name} -> {target.name} (event: '{event}')")
            self.change_state(target, actor)

    def handle_command(self, actor, command):
        next_state = self.current.handle_command(actor, command)
        if next_state is not None:
            self.change_state(next_state, actor)

    def update(self, actor, dt):
        next_state = self.current.update(actor, dt)
        if next_state is not None:
            self.change_state(next_state, actor)
