import sys
import os

# Add the root directory to the path in order to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import numpy as np

from src.solver.sudoku_solvers import backtracking_solver, lp_solver, degree_heuristic, mrv_heuristic, lcv_heuristic, random_heuristic

def test_backtracking_solver(grid, heuristic=None):
    solution = backtracking_solver(grid, heuristic=heuristic)
    if solution == 1:
        print("Unique solution exists.")
    elif solution == 2:
        print("More than one solution exists.")
    else:
        print("No solution exists.")
        
def test_lp_solver(grid):
    solution = lp_solver(grid)
    if solution == 1:
        print("Unique solution exists.")
    elif solution == 2:
        print("More than one solution exists.")
    else:
        print("No solution exists.")
        

def main():
    # Example of a Sudoku grid
    grid = np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])
    
    heursitics = [
        degree_heuristic,
        mrv_heuristic,
        lcv_heuristic,
        random_heuristic
    ]
    
    # Tests
    for heuristic in heursitics:
        print(f"Using {heuristic.__name__}:")
        test_backtracking_solver(grid, heuristic)
    test_backtracking_solver(grid)
    # test_lp_solver(grid)
    
if __name__ == "__main__":
    main()