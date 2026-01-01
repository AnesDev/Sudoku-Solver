import random

def is_valid(board, row, col, num):
    # Check row
    if num in board[row]: return False

    # Check column
    for r in range(9):
        if board[r][col] == num:
            return False

    # Check 3×3 box
    box_row = (row//3) * 3
    box_col = (col//3) * 3
    for r in range(box_row, box_row+3):
        for c in range(box_col, box_col+3):
            if board[r][c] == num:
                return False

    return True


def solve_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # empty
                nums = list(range(1,10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_full_grid():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_board(board)
    return board




def make_puzzle(board, difficulty="easy"):
    levels = {
        "easy": 40,
        "medium": 32,
        "hard": 25
    }
    
    puzzle = [row[:] for row in board]

    cells_to_remove = 81 - levels[difficulty]

    while cells_to_remove > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            cells_to_remove -= 1
    
    return puzzle


#solution = generate_full_grid()
#puzzle = make_puzzle(solution, difficulty="medium")

# puzzle is the matrix for your UI
#for row in puzzle:
#   print(row)
