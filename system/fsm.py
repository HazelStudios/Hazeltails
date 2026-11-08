class State:
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__

    def enter(self, actor):
        print(f"Entering state: {self.name}")

    def update(self, actor, dt):
        pass

    def exit(self, actor):
        print(f"Exiting state: {self.name}")

class FSM:
    def __init__(self, initial_state, actor=None):
        self.current = initial_state
        self.transitions = {} # (state, event) -> state
        if actor is not None:
            self.current.enter(actor)

    def add_transition(self, from_state, event, to_state):
        self.transitions[(from_state, event)] = to_state

    def trigger(self, event, actor):
        target = self.transitions.get((self.current, event))
        if target and target is not self.current:
            print(f"Transition: {self.current.name} -> {target.name} (event: '{event}')")
            self.current.exit(actor)
            self.current = target
            self.current.enter(actor)

    def update(self, actor, dt):
        self.current.update(actor, dt)
