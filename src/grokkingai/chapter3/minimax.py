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


def play_game(board: Connect4):
    player_move = True
    print("Welcome to Connect4 Minimax\n---\n")
    print(board)
    while board.get_valid_moves() and board.get_score_for_ai() == 0:
        while player_move:
            move = input("Human Move: ")
            try:
                board.play_move(int(move), 2)
                player_move = False
            except:
                if move.strip().lower() in ["exit", "clear"]:
                    print("Game Exited")
                    exit(0)
                print(f"Invalid Move please enter integer between 0 to {board.col - 1}")
        print(board)
        move = ai_move_random(board)
        print("AI Move:", move, "\n\n")
        board.play_move(move, 1)
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
