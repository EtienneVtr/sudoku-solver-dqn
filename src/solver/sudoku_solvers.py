import sys
import os

# Add the root directory to the path in order to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pulp
import numpy as np
import random

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
            
# Sudoku Solvers

def backtracking_solver(grid, solution_count=0, heuristic=None):
    """
    Solve the Sudoku grid using the backtracking algorithm and count the number of solutions.
    If more than one solution is found, stop and return 2.
    """
    # Check if the grid is valid
    if isinstance(grid, np.ndarray) and grid.ndim == 2 and grid.shape == (9, 9):
        print("Grid is valid!")
    else:
        raise ValueError("Invalid grid: It should be a 9x9 numpy array.")
    
    # If heuristic is provided, apply it to improve performance
    if heuristic:
        grid = heuristic(grid)

    # Try to find an empty cell
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:  # Empty cell found
                # Try all numbers from 1 to 9
                for num in range(1, 10):
                    if check_cell(grid, row, col, num):
                        grid[row][col] = num  # Place the number
                        
                        # Recurse to solve the rest of the grid
                        solution_count = backtracking_solver(grid, solution_count, heuristic)
                        
                        if solution_count == 2:  # If more than one solution is found, stop
                            return 2
                        
                        grid[row][col] = 0  # Backtrack, undo the move
                return solution_count  # No valid number found for this cell

    # If all cells are filled, we have found a solution
    solution_count += 1
    if solution_count > 1:  # If more than one solution is found, return 2
        return 2

    print("Solution found:")
    print(grid)

    return solution_count  # Only one solution found

def lp_solver(grid):
    """
    Solve the Sudoku grid using Linear Programming (LP).
    """
    # Create a linear programming problem
    prob = pulp.LpProblem("Sudoku", pulp.LpMinimize)

    # Create a dictionary of variables for the grid
    # x[i][j][k] will be 1 if cell (i,j) contains the number k, 0 otherwise
    x = {}
    for i in range(9):
        for j in range(9):
            for k in range(1, 10):
                x[i, j, k] = pulp.LpVariable(f"x_{i}_{j}_{k}", cat='Binary')

    # Add the constraints for each cell to have exactly one number
    for i in range(9):
        for j in range(9):
            prob += pulp.lpSum(x[i, j, k] for k in range(1, 10)) == 1

    # Add the constraints for each number to appear exactly once in each row
    for i in range(9):
        for k in range(1, 10):
            prob += pulp.lpSum(x[i, j, k] for j in range(9)) == 1

    # Add the constraints for each number to appear exactly once in each column
    for j in range(9):
        for k in range(1, 10):
            prob += pulp.lpSum(x[i, j, k] for i in range(9)) == 1

    # Add the constraints for each number to appear exactly once in each 3x3 subgrid
    for k in range(1, 10):
        for i in range(3):
            for j in range(3):
                prob += pulp.lpSum(x[3*i + m, 3*j + n, k] for m in range(3) for n in range(3)) == 1

    # Add the initial clues from the grid as constraints
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                prob += x[i, j, grid[i][j]] == 1
                for k in range(1, 10):
                    if k != grid[i][j]:
                        prob += x[i, j, k] == 0

    # Solve the problem
    prob.solve()

    # Extract the solution grid
    solution = np.zeros((9, 9), dtype=int)
    for i in range(9):
        for j in range(9):
            for k in range(1, 10):
                if pulp.value(x[i, j, k]) == 1:
                    solution[i][j] = k
                    break

    # If there's more than one solution, return 2
    if pulp.LpStatus[prob.status] != "Optimal":
        return 2

    '''print("Solution found:")
    print(solution)'''

    return 1

# Heuristic functions

def degree_heuristic(grid):
    """
    Degree Heuristic: prioritize the variables involved in the largest number of constraints.
    """
    pass

def random_heuristic(grid):
    """
    A simple random heuristic for variable ordering.
    """
    pass

def mrv_heuristic(grid):
    """
    Minimum Remaining Values (MRV) Heuristic: prioritize the variables with the fewest remaining values.
    """
    pass

def lcv_heuristic(grid, row, col):
    """
    Least Constraining Value (LCV) Heuristic: prioritize the values that rule out the fewest values in neighboring cells.
    """
    pass
