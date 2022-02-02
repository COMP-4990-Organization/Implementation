# Stores all the information needed to define a grid and draw it to a window

# Basic Imports
import pygame
import random

# Import the needed classes
from Node import Node
from Constants import Constants

# Implementation of the Grid class
class Grid:

    # Initializer for the Grid class
    # Takes a pygame window, rows of the grid, width of the grid
    # x and y offset if multiple grids want to be displayed on a single window
    # and cols if the number of rows and cols are different
    def __init__(self, win, rows, width, x_offset = 0, y_offset = 0, cols=0):
        self.win = win
        self.rows = rows
        if(cols==0):
            self.cols = rows
        else:
            self.cols = cols
        self.width = width
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.start = None
        self.end = None
        self.grid = []

        # Calculates the width of each Node
        gap = width // rows
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                self.grid[i].append(Node(i,j,gap, x_offset, y_offset, rows))

    # Sets all nodes in the grid to open (WHITE)
    def reset_grid(self):
        for row in self.grid:
            for spot in row:
                spot.reset()
        self.start = None
        self.end = None
    
    # Resets all Nodes that where opened or closed by a Search Algorithm
    def reset_search(self):
        for row in self.grid:
            for spot in row:
                if spot.is_start() or spot.is_end() or spot.is_barrier():
                    pass
                else:
                    spot.reset()
                    spot.draw(self.win)

    # Updates the neighbours of all the nodes in the Grid
    def update_neighbours(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbours(self.grid)

    # Draw the Grid to the pygame window
    def draw_grid(self):
        line_width = 1
        for row in self.grid:
            for spot in row:
                spot.draw(self.win)

        gap = self.width // self.rows
        for i in range(self.rows+1):
            if(i == 0 or i == self.rows):
                line_width = 3
            else:
                line_width = 1
            pygame.draw.line(self.win, Constants.GREY,(self.x_offset, self.y_offset + (i * gap)), (self.x_offset + self.width, self.y_offset + (i * gap)), line_width)
        
        # Will eventually change to using the cols variable
        for j in range(self.rows+1):
            if(j == 0 or j == self.rows):
                line_width = 3
            else:
                line_width = 1
            pygame.draw.line(self.win, Constants.GREY,(self.x_offset + (j * gap), self.y_offset), (self.x_offset + (j * gap), self.y_offset + self.width), line_width)

    # Copies a grid, used when multiple grids are used in one window so each grid can use
    # a different search algorithm on the same grid
    def copy_grid(self, grid):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].set_colour(grid.grid[i][j].get_colour())
                if(self.grid[i][j].is_start()):
                    self.start = self.grid[i][j]
                if(self.grid[i][j].is_end()):
                    self.end = self.grid[i][j]
    
    # Randomize the grid
    # Currently creates a random number of barriers between 0 and rows*col/2
    def randomize(self):
        self.reset_grid()
        start = (0,0)
        end = (0,0)

        # Keep creating new coordinates until the start and end are different
        while(start == end):
            start = (random.randrange(0,self.cols),random.randrange(0,self.rows))
            end = (random.randrange(0,self.cols),random.randrange(0,self.rows))

        # Update the start and end Nodes
        self.grid[start[0]][start[1]].make_start()
        self.grid[end[0]][end[1]].make_end()
        self.start = self.grid[start[0]][start[1]]
        self.end = self.grid[end[0]][end[1]]

        # Creates a random number of barriers
        for i in range(random.randrange(0,(self.rows*self.cols)//2)):
            blockade = (random.randrange(0,self.cols),random.randrange(0,self.rows))
            
            # Keep creating new coordinates until it is not the start or end
            while(blockade == start or blockade == end):
                blockade = (random.randrange(0,self.cols),random.randrange(0,self.rows))
            self.grid[blockade[0]][blockade[1]].make_barrier()

    # Writes the grid to a file
    def save_to_file(self, folderpath="Grids\\"):

        # Read the current number of Grids that have been written
        # in order to get a new filename
        number = 0
        with open("SearchWindow\\GridNumber", 'r', newline='') as infile:
            number = int(infile.read())
        number += 1
        number = str(number)
        filename = "Grid_" + number + ".txt"

        # Writes the grid to a file and adds surrounding barriers to the grid
        # because of this a 50x50 grid becomes a 52x52
        with open(folderpath+filename, "w") as outfile:
            for i in range(self.rows+2):
                outfile.write('1')
            outfile.write('\n')
            for row in self.grid:
                outfile.write('1')
                for spot in row:
                    outfile.write(Constants.switcher.get(spot.get_colour()))
                outfile.write('1\n')

            for i in range(self.rows+2):
                outfile.write('1')

        with open("SearchWindow\\GridNumber", 'w') as infile:
            infile.write(number)        