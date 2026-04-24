from copy import deepcopy
import os
import time


def find_order(num: int) -> int:
    if num < 0:
        return 1

    pow = 1

    while num // (10**pow):
        pow += 1

    return pow


def animate_path(maze, shortest_path, starting_point, shortest_distance, delay=0.3):
    while True:  # Loop forever (Ctrl+C to stop)
        for i, path in enumerate(shortest_path):
            # Move cursor to top (clear and redraw)
            os.system("clear")  # Use 'cls' on Windows

            print("Starting Position:", starting_point)
            print("Shortest Distance to Goal:", shortest_distance)
            print(f"Step: {i + 1}/{len(shortest_path)}")
            print()
            print(maze.__str__(path))

            time.sleep(delay)

        time.sleep(1)  # Pause at the end before looping


class Maze:
    def __init__(self, coordinates: list[list[int]], row: int, col: int):
        self.row = row
        self.col = col

        self.matrix = [[0] * col for _ in range(row)]

        for r, c, t in coordinates:
            self.matrix[r][c] = t

    def __str__(self, player_coord: tuple[int, int]) -> str:
        row_order = find_order(self.row - 1)
        col_order = find_order(self.col - 1)

        matrix = deepcopy(self.matrix)
        matrix[player_coord[0]][player_coord[1]] = "*"

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
