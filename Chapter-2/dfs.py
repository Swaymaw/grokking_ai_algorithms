from utils import Maze, animate_path

"""
0 -> Empty
1 -> Barrier
2 -> Goal
"""


def run_dfs(maze: Maze, current_point: tuple[int, int], visited_points: set = set()):
    matrix = maze.matrix
    stack = [(current_point, 0)]
    parent_map: dict[tuple[int, int], tuple[int, int] | None] = {current_point: None}
    while stack:
        (r, c), depth = stack.pop()
        visited_points.add((r, c))
        neighbors = maze.get_neighbors((r, c), include_diagonal=True)
        for neighbor in neighbors:
            if neighbor not in visited_points:
                stack.append((neighbor, depth + 1))
                parent_map[neighbor] = (r, c)
                if matrix[neighbor[0]][neighbor[1]] == "2":
                    path = []
                    cur_point = neighbor
                    while cur_point := parent_map.get(cur_point):
                        path.append(cur_point)
                    return path[::-1], (depth + 1,)

    return [], -1


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

    shortest_path, shortest_distance = run_dfs(maze, starting_point)

    if shortest_distance == -1:
        print("No Path Found")
    else:
        animate_path(maze, shortest_path, starting_point, shortest_distance)
