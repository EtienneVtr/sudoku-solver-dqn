import numpy as np
import os

difficulty = {"easy": 1, "medium": 2, "hard": 3, "expert": 4}

def generate_grid(difficulty="medium"):
    # Create a 9x9 grid of zeros
    grid = np.zeros((9, 9), dtype=int)
    
    # First, fill the diagonal 3x3 grids
    grid = fill_diagonal_grids(grid)
    
    # Then, fill the rest of the grid
    fill_remaining_grids(grid)
    
    # Save the grid as the solution before removing numbers
    save_grid(grid, difficulty, True)
    
    
    
    return grid

def fill_diagonal_grids(grid):
    for i in range(3):
        # Generate a random permutation of 1-9
        permutation = np.random.permutation(9) + 1
        # Fill the diagonal grid with the permutation
        grid[i*3:i*3+3, i*3:i*3+3] = permutation.reshape((3, 3))
        
    return grid

def fill_remaining_grids(grid):
    empty_cell = find_empty_cell(grid)  # Find an empty cell
    if not empty_cell:
        return True  # No empty cell, grid is complete
    
    row, col = empty_cell

    # Define a permutation of 1-9
    permutation = np.random.permutation(9) + 1
    
    for num in permutation:  # Try numbers from 1 to 9
        if check_cell(grid, row, col, num):  # Check if the number can be placed
            grid[row][col] = num  # Place the number
            
            if fill_remaining_grids(grid):  # Continue recursively
                return True
            
            grid[row][col] = 0  # Backtracking: undo the placement if it fails

    return False  # No valid number found for this cell

def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None  # No empty cell found

def check_cell(grid, row, col, num):
    # Verify the row
    if num in grid[row]:
        return False
    
    # Verify the column
    if num in grid[:, col]:
        return False
    
    # Verify the 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False

    return True

def check_grid(grid):
    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            if num == 0:
                return False
            if not check_cell(grid, i, j, num):
                return False
    return True

def save_grid(grid, difficulty, solution=False):
    # Path of the folder where the grids will be saved
    folder_path = os.path.join(os.path.dirname(__file__), "../../data/grids/")
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    
    # Count the number of existing files with the same difficulty
    existing_files = [f for f in os.listdir(folder_path) if f.startswith(f"solution_{difficulty}")]
    grid_number = len(existing_files) + 1  # Numéro de la grille

    # Name of the file
    if solution:
        file_name = f"solution_{difficulty}_{grid_number}.txt"
    else:
        file_name = f"grid_{difficulty}_{grid_number}.txt"
    file_path = os.path.join(folder_path, file_name)

    # Save the grid in the file
    with open(file_path, "w") as f:
        for row in grid:
            f.write(" ".join(map(str, row)) + "\n")  # Convert the row to a string of numbers separated by spaces
    
    print(f"Grid saved under the name : {file_path}")