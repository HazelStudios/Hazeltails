import pygame
from constants import (
    ACTION_IDLE,
    ACTION_RETURN,
    ACTION_SEARCH,
    ANIMATION_IDLE,
    ANIMATION_RETURN,
    ANIMATION_SEARCH,
)
from settings import NPC_REPATH_INTERVAL
from system.fsm import State


class _PathFollowMixin:

    def _get_spawn_foot(self, actor):
        return pygame.Vector2(
            actor.spawn[0] + actor.flyweight.size[0] / 2.0,
            actor.spawn[1] + actor.flyweight.size[1],
        )

    def _follow_current_path(self, actor) -> bool:
        if not actor.path:
            actor.velocity.x = 0
            return True

        waypoint, action = actor.path[0]
        foot = pygame.Vector2(actor.rect.midbottom)

        dx = waypoint.x - foot.x
        dy = waypoint.y - foot.y

        next_is_edge_action = len(actor.path) > 1 and actor.path[1][1] in ("jump", "drop")
        x_tolerance = 5 if next_is_edge_action else 12

        if action in ("jump", "drop"):
            reached = actor.on_ground and abs(dx) <= 16 and abs(dy) <= 10
        else:
            reached = abs(dx) <= x_tolerance and abs(dy) <= 18

        if reached:
            actor.path.pop(0)
            if not actor.path:
                actor.velocity.x = 0
                return True
            waypoint, action = actor.path[0]
            dx = waypoint.x - foot.x
            dy = waypoint.y - foot.y

        if abs(dx) > 3:
            direction = 1 if dx > 0 else -1
            actor.velocity.x = direction * actor.flyweight.speed
        else:
            actor.velocity.x = 0

        if action == "jump" and actor.on_ground:
            actor.velocity.y = -actor.flyweight.jump_speed
            actor.on_ground = False

        return False


class NPCIdleState(State):
    def enter(self, actor):
        super().enter(actor)
        actor.velocity.x = 0
        actor.path.clear()
        actor.set_animation(ANIMATION_IDLE)

    def handle_command(self, actor, command, value=None):
        if command == ACTION_SEARCH:
            return actor.flyweight.search_state
        return None


class NPCSearchState(State, _PathFollowMixin):
    def enter(self, actor):
        super().enter(actor)
        actor.repath_timer = 0.0
        actor.path.clear()
        actor.set_animation(ANIMATION_SEARCH)

    def update(self, actor, dt: float):
        if actor.target is None or actor.nav_graph is None:
            actor.fsm.trigger(ACTION_IDLE, actor)
            return

        if actor.rect.colliderect(actor.target.rect):
            actor.fsm.trigger(ACTION_RETURN, actor)
            return

        actor.repath_timer -= dt
        if actor.repath_timer <= 0.0 and actor.on_ground:
            actor.repath_timer = NPC_REPATH_INTERVAL
            actor.path = actor.nav_graph.find_path(
                actor.rect.midbottom,
                actor.target.rect.midbottom,
                max_range=actor.flyweight.search_range,
            )

        self._follow_current_path(actor)


class NPCReturnState(State, _PathFollowMixin):
    def enter(self, actor):
        super().enter(actor)
        actor.repath_timer = 0.0
        actor.set_animation(ANIMATION_RETURN)
        if actor.nav_graph is not None:
            actor.path = actor.nav_graph.find_path(
                actor.rect.midbottom,
                self._get_spawn_foot(actor),
                max_range=None,
            )

    def handle_command(self, actor, command, value=None):
        if command == ACTION_SEARCH:
            return actor.flyweight.search_state
        return None

    def update(self, actor, dt: float):
        spawn_foot = self._get_spawn_foot(actor)

        if not actor.path and actor.on_ground and actor.nav_graph is not None:
            actor.path = actor.nav_graph.find_path(
                actor.rect.midbottom,
                spawn_foot,
                max_range=None,
            )

        finished = self._follow_current_path(actor)
        dist_to_spawn = pygame.Vector2(actor.rect.midbottom).distance_to(spawn_foot)

        if finished or dist_to_spawn <= 16.0:
            actor.velocity.x = 0
            actor.fsm.trigger(ACTION_IDLE, actor)
