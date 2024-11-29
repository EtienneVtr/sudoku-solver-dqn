# Function to reset the grid
def reset_grid(initial_grid, grid):
    for i in range(9):
        for j in range(9):
            if not is_initial_cell(i, j, initial_grid):
                grid[i][j] = 0

# Function to check if a cell is from the initial grid
def is_initial_cell(row, col, initial_grid):
    return initial_grid[row][col] != 0