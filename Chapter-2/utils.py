def find_order(num: int) -> int:
    if num < 0:
        return 1

    pow = 1

    while num // (10**pow):
        pow += 1

    return pow


class Maze:
    def __init__(self, coordinates: list[list[int]], row: int, col: int):
        self.row = row
        self.col = col

        self.matrix = [[0] * col for _ in range(row)]

        for r, c, t in coordinates:
            self.matrix[r][c] = t

    def __str__(self) -> str:
        row_order = find_order(self.row - 1)
        col_order = find_order(self.col - 1)

        res = " " * (4 + row_order)
        res += " ".join([str(i) for i in range(0, self.col)])
        res += "\n" + " " * (row_order + 2)

        for c in range(self.col + 1):
            res += "_" * (find_order(c - 1)) + " "
        res += "\n"

        for r in range(self.row):
            res += f"{r}" + " " * (row_order - find_order(r) + 2) + "| "
            for c in range(self.col):
                res += str(self.matrix[r][c]) + " " * (find_order(c + 1))
            res += "\n"
        return res
