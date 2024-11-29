import sys
import os

# Add the root directory to the path in order to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pygame
import numpy as np

from src.generator.grid_generator import generate_grid
from src.solver.sudoku_solver import check_grid, place_hint
from src.utils.utils import reset_grid, is_initial_cell

# Display configuration
WINDOW_SIZE = 540 # window of 540x540 pixels (9x9 grid)
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
BUTTON_WIDTH = (WINDOW_SIZE-5*20)//4 # 4 buttons with 20px between them
BUTTON_HEIGHT = 40
BUTTON_GAP = 20 # 20px between the buttons

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
HIGHLIGHT_COLOR = (150, 150, 150)

# Pygame initialization
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE+2*BUTTON_GAP+BUTTON_HEIGHT))
pygame.display.set_caption("Sudoku")

# Initial grid example (remplace with your own grid)
solution_grid, grid = generate_grid()
initial_grid = np.copy(grid)

# Buttons
generate_button = pygame.Rect(BUTTON_GAP, WINDOW_SIZE + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
check_button = pygame.Rect(2*BUTTON_GAP+BUTTON_WIDTH, WINDOW_SIZE + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_button = pygame.Rect(3*BUTTON_GAP+2*BUTTON_WIDTH, WINDOW_SIZE + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
hint_button = pygame.Rect(4*BUTTON_GAP+3*BUTTON_WIDTH, WINDOW_SIZE + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)

# Selected cell
selected_cell = None

# List of non-correct cells
errors = []

# List of hints
hints = []

# Function to draw the grid
def draw_grid(win, highlight_cell, selected_cell=None):
    # Draw the Sudoku grid
    win.fill(GREY)
    
    # Highlight the cell under the mouse
    if (0 <= highlight_cell[0] < GRID_SIZE and 0 <= highlight_cell[1] < GRID_SIZE) and (highlight_cell != selected_cell):
        pygame.draw.rect(win, HIGHLIGHT_COLOR, (highlight_cell[1] * CELL_SIZE, highlight_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
    # Highlight the cells with errors
    for error in errors:
        pygame.draw.rect(win, (250, 180, 180), (error[1] * CELL_SIZE, error[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
    # Highlight the cells with hints
    for hint in hints:
        pygame.draw.rect(win, (180, 250, 180), (hint[1] * CELL_SIZE, hint[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
    # Highlight the selected cell
    if selected_cell is not None:
        pygame.draw.rect(win, (180, 180, 250), (selected_cell[1] * CELL_SIZE, selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Lines and columns
    for i in range(GRID_SIZE + 1):
        line_width = 3 if i % 3 == 0 else 1
        pygame.draw.line(win, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), line_width) # horizontal lines
        pygame.draw.line(win, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), line_width) # vertical lines
        
    # Draw buttons
    pygame.draw.rect(win, WHITE, generate_button)
    pygame.draw.rect(win, WHITE, check_button)
    pygame.draw.rect(win, WHITE, reset_button)
    pygame.draw.rect(win, WHITE, hint_button)

    # Text for buttons
    font = pygame.font.Font(None, 30)
    win.blit(font.render("New", True, BLACK), (generate_button.x + 35, generate_button.y + 10))
    win.blit(font.render("Verify", True, BLACK), (check_button.x + 25, check_button.y + 10))
    win.blit(font.render("Reset", True, BLACK), (reset_button.x + 30, reset_button.y + 10))
    win.blit(font.render("Help", True, BLACK), (hint_button.x + 35, hint_button.y + 10))

# Function to draw the numbers
def draw_numbers(win, grid):
    # Draw the numbers in the grid
    font = pygame.font.Font(None, 40)
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            if num != 0:
                text = font.render(str(num), True, BLACK)
                win.blit(text, (col * CELL_SIZE + (CELL_SIZE/2.5), row * CELL_SIZE + (CELL_SIZE/3)))
                
# Main loop
def main():
    global selected_cell
    global grid
    global errors
    global hints
    global initial_grid
    global solution_grid
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if generate_button.collidepoint(event.pos):
                    solution_grid, grid = generate_grid()
                    initial_grid = np.copy(grid)
                    errors = []
                    hints = []
                elif check_button.collidepoint(event.pos):
                    errors = check_grid(initial_grid, grid)
                elif reset_button.collidepoint(event.pos):
                    reset_grid(initial_grid, grid)
                    errors = []
                    hints = []
                elif hint_button.collidepoint(event.pos):
                    grid, hints = place_hint(solution_grid, grid, hints)
                else:
                    # Get the cell selected by the mouse
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = mouse_pos[1] // CELL_SIZE, mouse_pos[0] // CELL_SIZE

                    # Check if the selected cell is within the grid
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and not is_initial_cell(row, col, initial_grid) and not (row, col) in hints:
                        selected_cell = (row, col)
                        
            elif event.type == pygame.KEYDOWN:
                # Mapping keys to values
                key_to_value = {
                    pygame.K_1: 1, pygame.K_KP1: 1,
                    pygame.K_2: 2, pygame.K_KP2: 2,
                    pygame.K_3: 3, pygame.K_KP3: 3,
                    pygame.K_4: 4, pygame.K_KP4: 4,
                    pygame.K_5: 5, pygame.K_KP5: 5,
                    pygame.K_6: 6, pygame.K_KP6: 6,
                    pygame.K_7: 7, pygame.K_KP7: 7,
                    pygame.K_8: 8, pygame.K_KP8: 8,
                    pygame.K_9: 9, pygame.K_KP9: 9,
                    pygame.K_0: 0, pygame.K_KP0: 0,
                    pygame.K_BACKSPACE: 0,
                }

                # Check if the key corresponds to a value
                if event.key in key_to_value:
                    # Update the cell with the value associated with the key
                    grid[row][col] = key_to_value[event.key]
                    # Remove the cell from errors if it is correct
                    if selected_cell in errors:
                        errors.remove(selected_cell)
                    selected_cell = None
                
        # Highlight the cell under the mouse
        mouse_pos = pygame.mouse.get_pos()
        highlight_cell = (mouse_pos[1] // CELL_SIZE, mouse_pos[0] // CELL_SIZE)
        
        # Draw the grid and numbers
        draw_grid(window, highlight_cell, selected_cell) if selected_cell is not None else draw_grid(window, highlight_cell)
        draw_numbers(window, grid)
        
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()