# Allows for a Grid to be drawn, also allows for a random grid to be drawn.

# -------------Important keys--------------
# c = clear the screen (reset grid)
# Left click = First: Place start
#              Second: Place End
#              After the start and end are set, creates barriers
# Right Click = Remove start, end or barrier
# r = randomize grid
# s = save to file

# Basic Imports
import pygame

# Import needed classes

from GridUtil.Grid import Grid
from GridUtil.Constants import Constants

# Create the pygame window with specifics from the Constant class
WIN = pygame.display.set_mode((Constants.WIDTH, Constants.WIDTH))
pygame.display.set_caption("Grid_Creator")
ROWS = 10
 
def draw(win, grid, rows, width, min):
    if min == 0:
        win.fill(Constants.WHITE)

    grid.draw_grid()
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = x // gap
    col = y // gap
    return row, col

def main(win, width):
    # should be a perfect square 1,4,9, ...

    grid = Grid(WIN,ROWS,width)
 
    start = None
    end = None
    run = True

    # Run the interface and start the searching
    while run:
        # draw the grid
        draw(win, grid, ROWS, width, 0)

        # Checks events that have happened and acts accordingly
        for event in pygame.event.get():

            # If escape is pressed, exit the program
            if event.type == pygame.QUIT:
                run = False

            # If the left mouse button is pressed, then make the start, end
            # or blockade depending what has been set
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                col, row = get_clicked_pos(pos, ROWS, width)
                if(col > ROWS or row > ROWS):
                    continue
                spot = grid.grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                    grid.start = start
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                    grid.end = end
                elif spot != end and spot != start:
                    spot.make_barrier()

            # If the right mouse button is pressed, remove the start/stop/blockade that is on 
            # a certain block
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                col, row = get_clicked_pos(pos, ROWS, width)
                spot = grid.grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            # Keyboard button is pressed
            if event.type == pygame.KEYDOWN:
                # If s is pressed and start and end are set, then save the file
                if event.key == pygame.K_s and start and end:
                    grid.update_neighbours()
                    grid.save_to_file()
                
                # If r is pressed, then create a simple randomized grid
                if event.key == pygame.K_r:
                    grid.randomize()
                    start = True
                    end = True
                    
                # If c is pressed, then clear the board
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid.reset_grid()
    pygame.quit()

main(WIN, Constants.WIDTH)