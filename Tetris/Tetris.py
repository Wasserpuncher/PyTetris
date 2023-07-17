import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Shapes and their rotations
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1],
     [0, 0, 1]],
]

# Function to create a new shape
def new_shape():
    shape = random.choice(SHAPES)
    return shape

# Function to draw the shape on the grid
def draw_shape(screen, shape, row, col):
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == 1:
                pygame.draw.rect(screen, WHITE, ((col + c) * BLOCK_SIZE, (row + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to check for collisions
def check_collision(grid, shape, row, col):
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == 1:
                if row + r >= GRID_HEIGHT or col + c < 0 or col + c >= GRID_WIDTH or grid[row + r][col + c] != BLACK:
                    return True
    return False

# Function to update the grid with the current shape
def update_grid(grid, shape, row, col):
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == 1:
                grid[row + r][col + c] = WHITE

# Function to remove completed lines
def remove_lines(grid):
    lines_to_remove = [row for row in range(GRID_HEIGHT) if all(cell != BLACK for cell in grid[row])]
    for row in lines_to_remove:
        del grid[row]
        grid.insert(0, [BLACK] * GRID_WIDTH)

# Main function to run the game
def main():
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    # Create the clock
    clock = pygame.time.Clock()

    # Initialize the grid
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Variables for the game loop
    shape = new_shape()
    row = 0
    col = GRID_WIDTH // 2 - len(shape[0]) // 2
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Handle user input for moving the shape
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not check_collision(grid, shape, row, col - 1):
                col -= 1
        if keys[pygame.K_RIGHT]:
            if not check_collision(grid, shape, row, col + 1):
                col += 1
        if keys[pygame.K_DOWN]:
            if not check_collision(grid, shape, row + 1, col):
                row += 1

        # Move the shape down automatically
        if not check_collision(grid, shape, row + 1, col):
            row += 1
        else:
            update_grid(grid, shape, row, col)
            remove_lines(grid)
            shape = new_shape()
            row = 0
            col = GRID_WIDTH // 2 - len(shape[0]) // 2
            if check_collision(grid, shape, row, col):
                game_over = True

        # Clear the screen
        screen.fill(BLACK)

        # Draw the shape on the grid
        draw_shape(screen, shape, row, col)

        # Draw the grid
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                pygame.draw.rect(screen, grid[r][c], (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Update the display
        pygame.display.update()

        # Set the game speed
        clock.tick(5)

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()