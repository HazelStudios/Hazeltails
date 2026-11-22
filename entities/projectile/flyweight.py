class ProjectileFlyweight:

    def __init__(self, shared_state: dict):
        self._shared_state = shared_state
        self.radius: int = shared_state["radius"]
        self.speed: float = shared_state["speed"]
        self.lifetime: float = shared_state["lifetime"]
        self.cooldown: float = shared_state["cooldown"]
        self.color: tuple[int, int, int] = shared_state["color"]


class ProjectileFlyweightFactory:

    _flyweights: dict[str, ProjectileFlyweight] = {}

    def get_key(self, state: dict):
        return "_".join(f"{k}:{state[k]}" for k in sorted(state.keys()))

    def get_flyweight(self, shared_state: dict):
        key = self.get_key(shared_state)

        if not self._flyweights.get(key):
            self._flyweights[key] = ProjectileFlyweight(shared_state)

        return self._flyweights[key]
