import copy
import random

from grokkingai.utils import Connect4

"""
0 -> Empty
1 -> AI
2 -> Player
"""


def ai_move_random(board: Connect4):
    move = random.choice(board.get_valid_moves())
    return move


def ai_move_minmax(board: Connect4):
    def minmax(
        connect: Connect4, depth: int, alpha: float, beta: float, min_or_max: int
    ):
        score = connect.get_score_for_ai()
        board_full = len(connect.get_valid_moves()) == 0
        if score != 0 or board_full or depth == 0:
            return score

        best_score = -float("inf") * min_or_max
        moves = connect.get_valid_moves()
        random.shuffle(moves)
        for slot in moves:
            neighbor = copy.deepcopy(connect)
            neighbor.play_move(slot)

            score = minmax(neighbor, depth - 1, alpha, beta, min_or_max * -1)

            if min_or_max == 1:
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, score)
                beta = min(beta, best_score)

            if beta <= alpha:
                break

        return best_score

    best_move = None
    best_score = -float("inf")
    alpha = -float("inf")
    beta = float("inf")

    for slot in board.get_valid_moves():
        neighbor = copy.deepcopy(board)
        neighbor.play_move(slot)
        score = minmax(neighbor, depth=5, alpha=alpha, beta=beta, min_or_max=-1)

        if score > best_score:
            best_score = score
            best_move = slot

        alpha = max(alpha, best_score)

    return best_move


def play_game(board: Connect4):
    player_move = True
    print("Welcome to Connect4 Minimax\n---\n")
    print(board)
    while board.get_valid_moves() and board.get_score_for_ai() == 0:
        move = None
        while player_move:
            move = input("Human Move: ")
            try:
                board.play_move(int(move))
                player_move = False
            except:
                if move.strip().lower() in ["exit", "clear"]:
                    print("Game Exited")
                    exit(0)
                print(f"Invalid Move please enter integer between 0 to {board.col - 1}")

        if board.get_valid_moves() and board.get_score_for_ai() == 0:
            print(board)
            move = ai_move_minmax(board)
            if move is None:
                move = random.choice(board.get_valid_moves())
            print("AI Move:", move, "\n\n")
            board.play_move(move)
            player_move = True
            print(board)

    final_score = board.get_score_for_ai()

    if final_score > 0:
        print("Whoops! AI Won. Better Luck Next Time")
    elif final_score < 0:
        print("Wohoo! Human Won. Nice Win!")
    else:
        print("Hmm... We have a tie")


if __name__ == "__main__":
    board = Connect4(row=6, col=7)
    play_game(board)
