def find_empty(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None


def is_valid(grid, row, col, num):
    if num in grid[row]:
        return False

    for i in range(9):
        if grid[i][col] == num:
            return False
            
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False

    return True



def solve_sudoku(grid):
    empty = find_empty(grid)

    if not empty:
        return True

    row, col = empty

    for num in range(1, 10):  
        if is_valid(grid, row, col, num):
            grid[row][col] = num  

            if solve_sudoku(grid):
                return True

            grid[row][col] = 0  

    return False


def print_grid(grid):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            print(grid[i][j], end=" ")
        print()

