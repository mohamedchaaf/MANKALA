from mancala.play import Play


def display_board(board):
    print("\n================= MANCALA BOARD =================")
    # Player 2 pits
    print("          Player 2 (Computer)    ")
    p2_pits = ['G','H','I','J','K','L']
    print("  ", end="")
    for p in p2_pits:
        print(f"[{board[p]:2}]", end=" ")
    print()
    # Stores
    print(f"[{board[1]:2}]", " " * 25, f"[{board[2]:2}]")
    # Player 1 pits
    p1_pits = ['A','B','C','D','E','F']
    print("  ", end="")
    for p in p1_pits:
        print(f"[{board[p]:2}]", end=" ")
    print("\n          Player 1 (Human)")
    print("================================================\n")

def main():
    game = Play()
    display_board(game.game.state.board)

    while not game.game.gameOver():
        # Human turn
        extra = game.humanTurn()
        display_board(game.game.state.board)
        while extra:
            print("You get an extra turn!")
            extra = game.humanTurn()
            display_board(game.game.state.board)

        if game.game.gameOver():
            break

        # Computer turn
        extra = game.computerTurn()
        display_board(game.game.state.board)
        while extra:
            print("Computer gets an extra turn!")
            extra = game.computerTurn()
            display_board(game.game.state.board)

    winner, score = game.game.findWinner()
    print(f"Game Over! Winner: {winner} with {score} seeds.")

if __name__ == "__main__":
    main()

