import sys
import os

# Add the root directory to the path in order to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pygame
import numpy as np

from src.generator.grid_generator import generate_grid
from src.solver.sudoku_solver import check_grid, place_hint
from src.utils.utils import reset_grid

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

# Pygame initialization
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE+2*BUTTON_GAP+BUTTON_HEIGHT))
pygame.display.set_caption("Sudoku")

# Initial grid example (remplace with your own grid)
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Buttons
generate_button = pygame.Rect(BUTTON_GAP, WINDOW_SIZE + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
check_button = pygame.Rect(2*BUTTON_GAP+BUTTON_WIDTH, WINDOW_SIZE + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_button = pygame.Rect(3*BUTTON_GAP+2*BUTTON_WIDTH, WINDOW_SIZE + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)
hint_button = pygame.Rect(4*BUTTON_GAP+3*BUTTON_WIDTH, WINDOW_SIZE + BUTTON_GAP, BUTTON_WIDTH, BUTTON_HEIGHT)

# Function to draw the grid
def draw_grid(win):
    # Draw the Sudoku grid
    win.fill(GREY)
    
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
                text = font.render(str(num), True, WHITE)
                win.blit(text, (col * CELL_SIZE + (CELL_SIZE/2.5), row * CELL_SIZE + (CELL_SIZE/3)))
                
# Main loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if generate_button.collidepoint(event.pos):
                    generate_grid()
                elif check_button.collidepoint(event.pos):
                    check_grid()
                elif reset_button.collidepoint(event.pos):
                    reset_grid()
                elif hint_button.collidepoint(event.pos):
                    place_hint()
                
        # Draw the grid and numbers
        draw_grid(window)
        draw_numbers(window, grid)
        
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()