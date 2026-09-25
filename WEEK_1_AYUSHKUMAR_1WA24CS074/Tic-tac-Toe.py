def display_board(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def is_full(board):
    return ' ' not in board

def tic_tac_toe():
    print("AYUSH KUMAR USN_ 1WA24CS074")
    print("Tic-Tac-Toe! Positions are 0-8 (left-to-right, top-to-bottom)")

    while True: # Outer loop for playing multiple games
        board = [' '] * 9 # Initialize board for each new game

        # Set initial state as requested by the user
        board[0] = 'O'
        board[7] = 'O'
        board[8] = 'O'
        board[2] = 'X'
        board[3] = 'X'
        board[6] = 'X'

        while True: # Inner loop for a single game round
            display_board(board)

            while True:
                try:
                    move = int(input("Select an empty cell (0-8): "))
                    if 0 <= move <= 8 and board[move] == ' ':
                        board[move] = 'X'
                        break
                    else:
                        print("Invalid move. Cell is taken or out of range.")
                except ValueError:
                    print("Please enter a valid number.")

            if check_win(board, 'X'):
                display_board(board)
                print("Human Wins")
                break # Break from inner game loop

            if is_full(board):
                display_board(board)
                print("Draw")
                break # Break from inner game loop

            print("Computer is making a move...")
            moved = False

            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    if check_win(board, 'O'):
                        moved = True
                        break
                    board[i] = ' '

            if not moved:
                for i in range(9):
                    if board[i] == ' ':
                        board[i] = 'X'
                        if check_win(board, 'X'):
                            board[i] = 'O'
                            moved = True
                            break
                        board[i] = ' '

            if not moved:
                for i in range(9):
                    if board[i] == ' ':
                        board[i] = 'O'
                        break

            if check_win(board, 'O'):
                display_board(board)
                print("Computer Wins")
                break # Break from inner game loop

            if is_full(board):
                display_board(board)
                print("Draw")
                break # Break from inner game loop
        
        # After inner loop breaks (game over), ask to play again
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again not in ['yes', 'y']:
            break # Break from outer loop if not playing again

if __name__ == "__main__":
    tic_tac_toe()