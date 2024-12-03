# Sudoku Solver - DQN

## Author

**Etienne VATRY**

## Description

This project is a Sudoku Solver using a Deep Q-Network (DQN).

## Roadmap

### Creation of a Sudoku Game Interface (Done)
- Develop an interface with Pygame to play Sudoku

### Creation of a Sudoku puzzle generator (Done)
- Develop a Sudoku puzzle generator
- Create a grid which follows the rules of Sudoku
- Remove some numbers from the grid to create a puzzle
- The number of removed numbers depends on the difficulty level
- We also modify the number's distribution to make the puzzle more difficult
- The puzzle has at least one solution, but it can have more

### Creation of a Sudoku Solver (Not done)
- We want to create a Sudoku Solver using different algorithms
- The aim is to count the number of solutions for a given puzzle
- If a puzzle has only one solution, we can use it for the game. Otherwise, we need to generate another puzzle
- We will use:
  - Backtracking with different heuristics:
    - Degree heuristic
    - Random variable heuristic
    - MRV heuristic
    - LCV heuristic
  - Linear programming
- We will compare the different algorithms to find the best one in a Notebook

### Creation of a Sudoku Solver using a DQN (Not done)
- We want to create a Sudoku Solver using a DQN
- The aim is to train the DQN to solve Sudoku puzzles
- For this, we will use a dataset of Sudoku puzzles with their solutions (source: [Kaggle](https://www.kaggle.com/code/rohanrao/peter-norvig-s-sudoku-solver/input))

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/EtienneVtr/sudoku-solver-dqn.git
cd sudoku-solver-dqn
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

#### For the Sudoku Game Interface

```bash
python src/interface/sudoku_interface.py
```
