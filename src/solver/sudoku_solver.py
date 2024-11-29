import sys
import os

# Add the root directory to the path in order to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.generator.grid_generator import check_cell

# Function to return the errors in the grid
def check_grid(initial_grid, grid):
    errors = []
    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            if num != 0 and initial_grid[i][j] == 0:
                grid[i][j] = 0
                if not check_cell(grid, i, j, num):
                    errors.append((i, j))
                grid[i][j] = num
    return errors

# Function to place a hint in the grid
def place_hint(solution_grid, grid, hints):
    # Count the number of each digit in the grid
    count = [0] * 10
    for i in range(9):
        for j in range(9):
            count[grid[i][j]] += 1
    
    # Find the digit with the least occurrences
    min_count = min(count[1:])
    least_present_digit = count[1:].index(min_count) + 1
    if min_count == 9:
        return grid, hints
    
    # Find the first cell with the digit
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0 and solution_grid[i][j] == least_present_digit:
                hints.append((i,j))
                grid[i][j] = least_present_digit
                return grid, hints