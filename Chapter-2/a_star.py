import heapq
import itertools

from utils import Maze, animate_path


def get_path_cost(maze: Maze, path: list[tuple[int, int]]):
    total = 0
    for i in range(len(path) - 1):
        cost = maze.get_cost(path[i], path[i + 1])
        total += cost
    return total


def run_astar(maze: Maze, current_point: tuple[int, int], visited_points: set = set()):
    matrix = maze.matrix
    priority_queue: list = []
    goal_point = maze.get_goal_coords()
    parent_map: dict[tuple[int, int], tuple[int, int] | None] = {current_point: None}

    tie = itertools.count()
    heapq.heappush(priority_queue, (0, next(tie), current_point))
    while priority_queue:
        _, _, next_point = heapq.heappop(priority_queue)
        visited_points.add(next_point)

        path = []
        cur_point = next_point
        while cur_point := parent_map.get(cur_point):
            path.append(cur_point)
        path = path[::-1]
        path_cost = get_path_cost(maze, path + [next_point])

        if matrix[next_point[0]][next_point[1]] == "2":
            return path, path_cost

        for neighbor in maze.get_neighbors(next_point):
            if neighbor in visited_points:
                continue
            parent_map[neighbor] = next_point
            move_cost = maze.get_cost(next_point, neighbor)
            estimate = abs(goal_point[0] - neighbor[0]) + abs(
                goal_point[1] - neighbor[1]
            )
            heapq.heappush(
                priority_queue, (path_cost + move_cost + estimate, next(tie), neighbor)
            )

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
    maze = Maze(
        coordinates,
        row,
        col,
        weights={
            (0, 1): 1,
            (1, 0): 5,
            (0, -1): 1,
            (-1, 0): 5,
        },
    )
    shortest_path, shortest_distance = run_astar(maze, starting_point)

    if shortest_distance == -1:
        print("No Path Found")
    else:
        animate_path(maze, shortest_path, starting_point, shortest_distance)
