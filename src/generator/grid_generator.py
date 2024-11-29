import numpy as np
import os

difficulty_levels = {"easy": 1, "medium": 2, "hard": 3, "expert": 4}

# Function to generate a Sudoku grid
def generate_grid(difficulty="hard"):
    # Create a 9x9 grid of zeros
    grid = np.zeros((9, 9), dtype=int)
    
    # First, fill the diagonal 3x3 grids
    grid = fill_diagonal_grids(grid)
    
    # Then, fill the rest of the grid
    fill_remaining_grids(grid)
    
    # Save the grid as the solution before removing numbers
    save_grid(grid, difficulty, True)
    solution_grid = np.copy(grid)
    
    # Remove numbers from the grid to create the puzzle
    remove_numbers(grid, difficulty)
    
    return solution_grid, grid

# Function to fill the diagonal 3x3 grids with random permutations of 1-9
def fill_diagonal_grids(grid):
    for i in range(3):
        # Generate a random permutation of 1-9
        permutation = np.random.permutation(9) + 1
        # Fill the diagonal grid with the permutation
        grid[i*3:i*3+3, i*3:i*3+3] = permutation.reshape((3, 3))
        
    return grid

# Function to fill the remaining empty cells of the grid
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

# Function to find an empty cell in the grid
def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None  # No empty cell found

# Function to check if a cell is valid, i.e., if the number can be placed in the cell
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

# Function to check if the grid is valid
def check_grid(grid):
    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            if num == 0:
                return False
            if not check_cell(grid, i, j, num):
                return False
    return True

# Function to save the grid to a file
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
    
# Function to remove numbers from the grid to create the puzzle
def remove_numbers(grid, difficulty):
    # Determine how many cells to remove
    n_cells = min(np.random.randint(9, 12) * (difficulty_levels[difficulty] + 2), 64) # Example for difficulty = 'medium' :
                                                                                      # n_cells ~= min(10*(2+2), 64) = 40
                                                                                      
    # Generate a distribution of numbers
    target_distribution = generate_distribution(difficulty, n_cells)
    current_counts = np.sum(grid != 0, axis=0).tolist()  # Count of current numbers
    
    # Shuffle the cells to remove them randomly
    permutation = np.random.permutation(81)
    
    i = 0
    while n_cells > 0 and i < 81:
        row, col = permutation[i] // 9, permutation[i] % 9
        num = grid[row][col]
        
        # Check if we can remove this cell while respecting the distribution
        if num != 0 and current_counts[num - 1] > target_distribution[num - 1]:
            grid[row][col] = 0
            current_counts[num - 1] -= 1
            n_cells -= 1
            
        i += 1
      
# Function to generate a distribution of numbers to remove  
def generate_distribution(difficulty, n_cells):
    # Define means and standard deviations for each difficulty
    difficulty_params = {
        "easy": {"mean": 9, "std": 1},    # High mean, tight distribution
        "medium": {"mean": 7, "std": 2},  # Intermediate mean
        "hard": {"mean": 5, "std": 3},    # Low mean, more variation
        "expert": {"mean": 3, "std": 4},  # Very low mean, high variation
    }
    
    params = difficulty_params[difficulty]
    
    # Generate a normal distribution for 9 numbers
    raw_distribution = np.random.normal(loc=params["mean"], scale=params["std"], size=9)
    
    # Convert to integers and adjust to stay within realistic bounds
    distribution = np.clip(np.round(raw_distribution), 1, 9).astype(int)
    
    # Calculate the total number of cells to retain
    n_retained_cells = 81 - n_cells
    
    # Adjust the distribution to match the total retained cells
    while sum(distribution) > n_retained_cells:  # Too many numbers
        for i in range(9):
            if distribution[i] > 1:  # Reduce larger numbers first
                distribution[i] -= 1
                if sum(distribution) == n_retained_cells:
                    break
    
    while sum(distribution) < n_retained_cells:  # Too few numbers
        for i in range(9):
            if distribution[i] < 9:  # Increase smaller numbers first
                distribution[i] += 1
                if sum(distribution) == n_retained_cells:
                    break
    
    # Shuffle the order of the numbers for randomness
    np.random.shuffle(distribution)
        
    return distribution