import pygame


class SpatialGrid:
    """Only checks collitions on items on the same cell"""

    def __init__(self, cell_size: int):
        self.cell_size = cell_size
        self.cells: dict[tuple[int, int], list] = {}

    def cells_for(self, rect):
        size = self.cell_size
        for x in range(rect.left // size, (rect.right - 1) // size + 1):
            for y in range(rect.top // size, (rect.bottom - 1) // size + 1):
                yield x, y

    def insert(self, item, rect):
        for cell in self.cells_for(rect):
            self.cells.setdefault(cell, []).append(item)

    def query(self, rect) -> list:
        """Candidates near rect"""
        found = []
        for cell in self.cells_for(rect):
            found.extend(self.cells.get(cell, ()))
        return found

    def clear(self):
        self.cells.clear()
