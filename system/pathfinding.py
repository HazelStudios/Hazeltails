import heapq
import math
from typing import Optional
import pygame
from settings import FIXED_DT, GRAVITY, MAX_FALL_SPEED, NPC_JUMP_SPEED, NPC_SPEED, NPC_WAYPOINT_STEP


class PlatformNavGraph:

    def __init__(self, platforms: list[pygame.Rect], entity_size: tuple[int, int]):
        self.entity_width, self.entity_height = entity_size
        self.walkable: list[pygame.Rect] = [
            p for p in platforms if p.left >= 0 and p.width >= self.entity_width
        ]
        self.nodes: list[pygame.Vector2] = []
        self.node_platform: list[int] = []
        self.edges: dict[int, list[tuple[int, float, str]]] = {}
        self._build_nodes()

    def _build_nodes(self):
        half_w = self.entity_width // 2

        for p_idx, plat in enumerate(self.walkable):
            start_x = plat.left + half_w
            end_x = plat.right - half_w
            if start_x >= end_x:
                xs = [plat.centerx]
            else:
                xs = list(range(start_x, end_x + 1, NPC_WAYPOINT_STEP))
                if xs[-1] != end_x:
                    xs.append(end_x)

            for x in xs:
                self.nodes.append(pygame.Vector2(x, plat.top))
                self.node_platform.append(p_idx)

    # Simulate a jump from start to target and check if it is possible without hitting any platforms
    def _simulate_jump(
        self,
        start: pygame.Vector2,
        target: pygame.Vector2,
        source_plat: pygame.Rect,
        target_plat: pygame.Rect,
        platforms: list[pygame.Rect],
    ):
        if target.x > start.x:
            direction = 1.0
        else:
            direction = -1.0

        pos = pygame.Vector2(start.x - self.entity_width / 2.0, start.y - self.entity_height)
        vel = pygame.Vector2(direction * NPC_SPEED, -NPC_JUMP_SPEED)
        sim_rect = pygame.Rect(round(pos.x), round(pos.y), self.entity_width, self.entity_height)

        # Simulate up to 2.5 seconds of flight
        max_steps = int(2.5 / FIXED_DT)
        for _ in range(max_steps):
            prev_bottom = pos.y + self.entity_height
            vel.y = min(vel.y + GRAVITY * FIXED_DT, MAX_FALL_SPEED)

            # Move X and check wall/side collisions
            pos.x += vel.x * FIXED_DT
            sim_rect.x = round(pos.x)

            for plat in platforms:
                if plat is source_plat or plat.left < 0:
                    continue
                if sim_rect.colliderect(plat):
                    return False

            # Move Y and check ceiling / landing collisions
            pos.y += vel.y * FIXED_DT
            sim_rect.y = round(pos.y)

            for plat in platforms:
                if plat is source_plat or plat.left < 0:
                    continue
                if sim_rect.colliderect(plat):
                    if vel.y < 0:
                        return False
                    if vel.y > 0 and prev_bottom <= plat.top + 2.0:
                        if plat is target_plat and abs(sim_rect.centerx - target.x) <= NPC_WAYPOINT_STEP * 0.75:
                            return True
                        return False

            if vel.y > 0 and (pos.y + self.entity_height) > target.y + 16.0:
                return False

        return False

    def _get_edges(self, i: int):
        if i in self.edges:
            return self.edges[i]

        a = self.nodes[i]
        half_w = self.entity_width // 2
        plat_a = self.walkable[self.node_platform[i]]
        is_left_edge_a = abs(a.x - (plat_a.left + half_w)) <= 4
        is_right_edge_a = abs(a.x - (plat_a.right - half_w)) <= 4
        is_edge_a = is_left_edge_a or is_right_edge_a

        # Filter only platforms within jump reach so simulation stays fast on huge maps
        reach_margin = 320.0 + self.entity_width
        nearby_platforms = [
            p for p in self.walkable if p.right >= a.x - reach_margin and p.left <= a.x + reach_margin
        ]

        node_edges: list[tuple[int, float, str]] = []

        for j, b in enumerate(self.nodes):
            if i == j:
                continue

            dx = abs(a.x - b.x)
            if dx > 320.0:
                continue

            plat_b = self.walkable[self.node_platform[j]]
            dy = b.y - a.y

            # Walk along the same platform
            if self.node_platform[i] == self.node_platform[j]:
                if dx <= NPC_WAYPOINT_STEP * 1.25:
                    node_edges.append((j, dx, "walk"))
                continue

            # Drop down from an elevated platform's left or right edge
            if dy > 16:
                if is_edge_a and dx <= 200.0:
                    drop_clearance = half_w + 10.0
                    valid_left_drop = is_left_edge_a and b.x <= (plat_a.left - drop_clearance)
                    valid_right_drop = is_right_edge_a and b.x >= (plat_a.right + drop_clearance)
                    if valid_left_drop or valid_right_drop:
                        node_edges.append((j, a.distance_to(b) + 15.0, "drop"))
                continue

            # Jump across a gap or up onto a higher platform
            if abs(dy) <= 16 and not is_edge_a:
                continue

            # Check impossible jump heights before simulating
            if -dy > NPC_JUMP_SPEED ** 2 / (2 * GRAVITY):
                continue

            if self._simulate_jump(a, b, plat_a, plat_b, nearby_platforms):
                cost = math.hypot(dx, dy * 1.3) + 30.0
                node_edges.append((j, cost, "jump"))

        self.edges[i] = node_edges
        return node_edges

    def get_nearest_node(self, point):
        if not self.nodes:
            return None
        p = pygame.Vector2(point)
        return min(
            range(len(self.nodes)),
            key=lambda idx: (self.nodes[idx].x - p.x) ** 2 + ((self.nodes[idx].y - p.y) * 3.0) ** 2,
        )

    def find_path(self, start_pos: pygame.Vector2, goal_pos: pygame.Vector2, max_range = None):
        start_vec = pygame.Vector2(start_pos)
        goal_vec = pygame.Vector2(goal_pos)

        if max_range is not None:
            if start_vec.distance_to(goal_vec) > max_range:
                return []

        start_idx = self.get_nearest_node(start_vec)
        goal_idx = self.get_nearest_node(goal_vec)
        if start_idx is None or goal_idx is None:
            return []

        if start_idx == goal_idx:
            return [(goal_vec, "walk")]

        open_heap: list[tuple[float, int]] = [(0.0, start_idx)]
        came_from: dict[int, tuple[int, str]] = {}
        g_score: dict[int, float] = {start_idx: 0.0}

        goal_node = self.nodes[goal_idx]

        while open_heap:
            _, current = heapq.heappop(open_heap)

            if current == goal_idx:
                path: list[tuple[pygame.Vector2, str]] = []
                curr = current
                while curr in came_from:
                    prev, action = came_from[curr]
                    path.append((self.nodes[curr].copy(), action))
                    curr = prev
                path.append((self.nodes[start_idx].copy(), "walk"))
                path.reverse()
                path.append((goal_vec, "walk"))
                
                # Remove the first waypoint if it is in the same direction as the next one to avoid unnecessary backtracking
                if len(path) > 1 and path[1][1] == "walk":
                    to_next = path[1][0].x - start_vec.x
                    from_start = start_vec.x - path[0][0].x
                    if (to_next > 0 and from_start > 0) or (to_next < 0 and from_start < 0):
                        path.pop(0)

                return path

            # Uses lazy edge computation with cache
            for neighbor, weight, action in self._get_edges(current):
                tentative_g = g_score[current] + weight
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = (current, action)
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.nodes[neighbor].distance_to(goal_node)
                    heapq.heappush(open_heap, (f_score, neighbor))

        return []
