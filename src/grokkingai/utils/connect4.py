"""
0 -> Empty
1 -> AI
2 -> Player
"""


class Connect4:
    def __init__(self, row: int, col: int, win_len=4):
        self.row = row
        self.col = col
        self.win_len = 4
        self.matrix = [[0] * col for _ in range(self.row)]

    def get_valid_moves(self):
        moves = []
        for c in range(self.col):
            if self.matrix[0][c] == 0:
                moves.append(c)
        return moves

    def check_horizontal(self, player):
        max_window = 0
        for row in range(self.row):
            current = 0
            for c in range(self.col):
                if self.matrix[row][c] == player:
                    current += 1
                    max_window = max(max_window, current)
                else:
                    current = 0
        return max_window

    def check_vertical(self, player):
        max_window = 0
        for col in range(self.col):
            current = 0
            for r in range(self.row):
                if self.matrix[r][col] == player:
                    current += 1
                    max_window = max(max_window, current)
                else:
                    current = 0

        return max_window

    def check_diagonal(self, player):
        def count_diagonal(start_r, start_c, dr, dc):
            current = max_win = 0
            r, c = start_r, start_c
            while 0 <= r < self.row and 0 <= c < self.col:
                if self.matrix[r][c] == player:
                    current += 1
                    max_win = max(current, max_win)
                else:
                    current = 0
                r += dr
                c += dc

            return max_win

        max_window = 0

        for r in range(self.row):
            max_window = max(
                max_window,
                count_diagonal(
                    r, 0, 1, 1
                ),  # left edge (primary: top left -> bottom right)
                count_diagonal(
                    r, self.col - 1, 1, -1
                ),  # right edge (secondary: top right -> bottom left)
            )
        for c in range(self.col):
            max_window = max(
                max_window,
                count_diagonal(
                    0, c, 1, 1
                ),  # top row (primary: top left -> bottom right)
                count_diagonal(
                    0, c, 1, -1
                ),  # top row (secondary: top right -> bottom left)
            )

        return max_window

    def get_score_for_ai(self):
        max_window_ai = max(
            self.check_horizontal(1), self.check_vertical(1), self.check_diagonal(1)
        )
        max_window_player = max(
            self.check_horizontal(2), self.check_vertical(2), self.check_diagonal(2)
        )
        if max_window_ai >= self.win_len:
            return 10
        elif max_window_player >= self.win_len:
            return -10
        else:
            return 0

    def play_move(self, move: int, player: int):
        if move not in self.get_valid_moves():
            raise ValueError("Invalid Move")

        for r in range(self.row - 1, -1, -1):
            if self.matrix[r][move] == 0:
                self.matrix[r][move] = player
                return

    def __str__(self):
        val = ""
        for r in range(self.row):
            for c in range(self.col):
                val += str(self.matrix[r][c]) + " "
            val += "\n"
        return val
