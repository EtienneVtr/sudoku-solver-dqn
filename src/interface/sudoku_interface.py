import pygame
import numpy as np

# Display configuration
WINDOW_SIZE = 540 # window of 540x540 pixels (9x9 grid)
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Pygame initialization
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku")

# Initial grid example (remplace with your own grid)
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Function to draw the grid
def draw_grid(win):
    # Draw the Sudoku grid
    win.fill(WHITE)
    
    # Lines and columns
    for i in range(GRID_SIZE + 1):
        line_width = 3 if i % 3 == 0 else 1
        pygame.draw.line(win, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), line_width) # horizontal lines
        pygame.draw.line(win, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), line_width) # vertical lines
        
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
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Draw the grid and numbers
        draw_grid(window)
        draw_numbers(window, grid)
        
        pygame.display.update()
        
    pygame.quit()
    
if __name__ == "__main__":
    main()