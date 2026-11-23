import logging
from constants import ACTION_IDLE, ACTION_RETURN, ACTION_SEARCH
from entities.npc.npc_states import NPCIdleState, NPCReturnState, NPCSearchState

logger = logging.getLogger(__name__)


class NPCFlyweight:

    def __init__(self, shared_state: dict):
        self._shared_state = shared_state
        self.size: tuple[int, int] = shared_state["size"]
        self.speed: float = shared_state["speed"]
        self.jump_speed: float = shared_state["jump_speed"]
        self.search_range: float = shared_state["search_range"]
        self.color: tuple[int, int, int] = shared_state["color"]

        self.idle_state = NPCIdleState()
        self.search_state = NPCSearchState()
        self.return_state = NPCReturnState()

        self.transitions = {
            (self.idle_state, ACTION_SEARCH): self.search_state,
            (self.search_state, ACTION_RETURN): self.return_state,
            (self.search_state, ACTION_IDLE): self.idle_state,
            (self.return_state, ACTION_IDLE): self.idle_state,
            (self.return_state, ACTION_SEARCH): self.search_state,
        }


class NPCFlyweightFactory:

    def __init__(self, initial_flyweights: list[dict]):
        self._flyweights: dict[str, NPCFlyweight] = {}
        for state in initial_flyweights:
            self._flyweights[self.get_key(state)] = NPCFlyweight(state)

    def get_key(self, state: dict):
        return "_".join(f"{k}:{state[k]}" for k in sorted(state.keys()))

    def get_flyweight(self, shared_state: dict):
        key = self.get_key(shared_state)

        if not self._flyweights.get(key):
            logger.debug("NPCFlyweightFactory: Can't find a flyweight, creating new one.")
            self._flyweights[key] = NPCFlyweight(shared_state)
        else:
            logger.debug("NPCFlyweightFactory: Reusing existing flyweight.")

        return self._flyweights[key]

    def list_flyweights(self):
        count = len(self._flyweights)
        logger.debug("NPCFlyweightFactory: I have %d flyweights:", count)
        for key in self._flyweights:
            logger.debug(" - %s", key)
