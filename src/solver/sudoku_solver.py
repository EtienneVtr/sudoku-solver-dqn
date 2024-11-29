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

def place_hint():
    print("Placing hint")
    return