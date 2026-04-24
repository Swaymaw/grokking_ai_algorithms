from collections import deque
from utils import Maze, animate_path

"""
0 -> Empty
1 -> Barrier
2 -> Goal
"""


def run_bfs(
    matrix: list[list[int]], current_point: tuple[int, int], visited_points: set = set()
):
    queue = deque()
    queue.append((current_point, 0))
    visited_points.add(current_point)

    parent_map = {current_point: None}
    while queue:
        (r, c), depth = queue.popleft()
        neighbors = []
        if r > 0 and matrix[r - 1][c] != 1:
            neighbors.append((r - 1, c))
        if c > 0 and matrix[r][c - 1] != 1:
            neighbors.append((r, c - 1))
        if r < row - 1 and matrix[r + 1][c] != 1:
            neighbors.append((r + 1, c))
        if c < col - 1 and matrix[r][c + 1] != 1:
            neighbors.append((r, c + 1))

        for neighbor in neighbors:
            if neighbor not in visited_points:
                parent_map[neighbor] = (r, c)
                queue.append((neighbor, depth + 1))
                visited_points.add(neighbor)
                if matrix[neighbor[0]][neighbor[1]] == 2:
                    path = []
                    cur_point = neighbor
                    while cur_point := parent_map.get(cur_point):
                        path.append(cur_point)
                    return path[::-1], depth + 1

    return "No Path Found"


if __name__ == "__main__":
    coordinates = [
        [0, 0, 2],
        [1, 1, 1],
        [1, 2, 1],
        [1, 3, 1],
        [2, 1, 1],
        [3, 1, 1],
        [2, 3, 1],
    ]
    starting_point = (2, 2)
    row, col = 5, 5

    # Processing
    maze = Maze(coordinates, row, col)

    shortest_path, shortest_distance = run_bfs(maze.matrix, starting_point)
    animate_path(maze, shortest_path, starting_point, shortest_distance)
