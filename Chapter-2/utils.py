import os
import time
from copy import deepcopy


def find_order(num: int) -> int:
    if num < 0:
        return 1

    pow = 1

    while num // (10**pow):
        pow += 1

    return pow


def animate_path(maze, shortest_path, starting_point, shortest_distance, delay=0.3):
    while True:
        for i, path in enumerate(shortest_path):
            os.system("clear")

            print("Starting Position:", starting_point)
            print("Shortest Distance to Goal:", shortest_distance)
            print(f"Step: {i + 1}/{len(shortest_path)}")
            print()
            print(maze.to_string(path))

            time.sleep(delay)

        time.sleep(1)


class Maze:
    def __init__(
        self,
        coordinates: list[list[int]],
        row: int,
        col: int,
        weights: dict[tuple[int, int], int] = {
            (0, 1): 1,
            (1, 0): 1,
            (0, -1): 1,
            (-1, 0): 1,
        },
    ):
        self.row = row
        self.col = col
        self.weights = weights
        self.coordinates = coordinates

        self.matrix = [["0"] * col for _ in range(row)]

        for r, c, t in coordinates:
            self.matrix[r][c] = str(t)

    def get_goal_coords(self):
        for r, c, val in self.coordinates:
            if val == "2":
                return (r, c)
        return (0, 0)

    def get_cost(self, parent: tuple[int, int], neighbor: tuple[int, int]):
        x1, y1 = parent
        x2, y2 = neighbor
        x = x2 - x1
        y = y2 - y1

        return self.weights.get((x, y), 1)

    def get_neighbors(
        self, coord: tuple[int, int], include_diagonal: bool = False
    ) -> list[tuple[int, int]]:
        r, c = coord
        neighbors = []

        if r > 0 and self.matrix[r - 1][c] != "1":
            neighbors.append((r - 1, c))
        if c > 0 and self.matrix[r][c - 1] != "1":
            neighbors.append((r, c - 1))
        if r < self.row - 1 and self.matrix[r + 1][c] != "1":
            neighbors.append((r + 1, c))
        if c < self.col - 1 and self.matrix[r][c + 1] != "1":
            neighbors.append((r, c + 1))

        if include_diagonal:
            if c < self.col - 1:
                if r < self.row - 1 and self.matrix[r + 1][c + 1] != "1":
                    neighbors.append((r + 1, c + 1))
                if r > 0 and self.matrix[r - 1][c + 1] != "1":
                    neighbors.append((r - 1, c + 1))
            if c > 0:
                if r < self.row - 1 and self.matrix[r + 1][c - 1] != "1":
                    neighbors.append((r + 1, c - 1))
                if r > 0 and self.matrix[r - 1][c - 1] != "1":
                    neighbors.append((r - 1, c - 1))
        return neighbors

    def to_string(self, player_coord: tuple[int, int] | None = None) -> str:
        row_order = find_order(self.row - 1)
        matrix = deepcopy(self.matrix)
        if player_coord is not None:
            row, col = player_coord
            matrix[row][col] = "*"

        res = " " * (4 + row_order)
        res += " ".join([str(i) for i in range(0, self.col)])
        res += "\n" + " " * (row_order + 2)

        for c in range(self.col + 1):
            res += "_" * (find_order(c - 1)) + " "
        res += "\n"

        for r in range(self.row):
            res += f"{r}" + " " * (row_order - find_order(r) + 2) + "| "
            for c in range(self.col):
                res += str(matrix[r][c]) + " " * (find_order(c + 1))
            res += "\n"
        return res

    def __str__(self):
        return self.to_string()
