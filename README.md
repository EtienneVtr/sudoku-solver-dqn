# Sudoku Solver - DQN

## Author

**Etienne VATRY**

## Description

This project is a Sudoku Solver using a Deep Q-Network (DQN).

## Roadmap

### Creation of a Sudoku Game Interface
- Develop an interface (e.g., Pygame or Tkinter) to visualize the grid state, agent actions, and its progress in real-time. This will also be used to observe results during training.

### Creation of a Sudoku Grid Generator
- Design a grid generator capable of producing Sudokus of varying difficulty levels. This will allow testing the agent on increasingly complex levels.
- Create grids with multiple solutions and others with a unique solution to diversify training scenarios.

### Creation of a Grid Validity Function
- Code a function that validates each attempt by the agent: check rows, columns, and sub-grids for duplicates or inconsistencies.
- Record errors to assign penalties and adjust rewards based on the agent's actions, guiding its learning.
- Implement real-time validation so the agent receives immediate positive or negative feedback after each action.

### Creation of a Sudoku Grid Solver
- Program an exact solver (e.g., using backtracking) to solve the grids. It will serve as a "reference" to evaluate the agent's performance at each training stage.
- Use the solver to test the agent and validate the accuracy of its solutions by comparing the agent's final grid with the exact solution.

### Implementation of the DQN (Deep Q-Network)
- Design the architecture of your DQN with a dense neural network (or convolutional to capture spatial relationships in the grid). You can use libraries like PyTorch or TensorFlow to build and train the model.
- Define the state space as the current Sudoku grid and the action space as the values the agent can place in each cell.
- Implement an experience replay mechanism (replay buffer) to store experiences (state, action, reward, next state) and train the network in batches.

### Definition of the Reward and Penalty System
- Assign small rewards for each correctly placed cell and penalties for each action creating duplicates (in row, column, or sub-grid).
- Add a large reward for each grid completed without errors to maximize the agent's learning on valid grids.
- Adjust the balance between rewards and penalties to guide the agent to follow Sudoku rules over episodes.

### Curriculum Learning: Progressive Training
- Train the agent first on simple grids, then gradually increase the difficulty to improve its ability to solve more complex Sudokus.
- Enrich the agent's experience by confronting it with varied grids (different initial fill levels) to get used to new contexts.

### Training the DQN
- Run training sessions and adjust hyperparameters (learning rate, gamma for cumulative reward, epsilon for exploration) to optimize learning.
- Monitor model convergence and observe if the agent achieves better cumulative scores over time.

### Visualization of Training Progress
- Record different training epochs and plot graphs to track the evolution of cumulative rewards, error rates, and resolution times.
- Add logs and display in real-time the actions chosen by the agent with their Q-values to facilitate debugging and analysis of the agent's decisions.

### Testing and Validation of the DQN Model
- Test the agent on grids not present in the training dataset to verify its generalization ability.
- Compare the solutions found by the agent with those of the reference solver to validate its efficiency and accuracy.

### Optimization and Final Adjustments
- Fine-tune hyperparameters and adjust the reward system to correct any biases in the agent's behavior.
- Test the model's stability to solve more complex grids and observe if modifications (like a convolutional network) could improve performance.
