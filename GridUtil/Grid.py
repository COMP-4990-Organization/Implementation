# Stores all the information needed to define a grid and draw it to a window

# Basic Imports
import pygame
import random
from math import floor,sqrt
from os.path import exists

# Import the needed classes
from GridUtil.Node import Node
from GridUtil.Constants import Constants

# Implementation of the Grid class
class Grid:

    # Initializer for the Grid class
    # Takes a pygame window, rows of the grid, width of the grid
    # x and y offset if multiple grids want to be displayed on a single window
    # and cols if the number of rows and cols are different
    def __init__(self, win, rows, width, cols=0, weights = -1):
        self.win = win
        self.rows = rows
        if(cols==0):
            self.cols = rows
        else:
            self.cols = cols
        self.width = width
        self.start = None
        self.end = None
        self.grid = []
        if win == None:
            self.drawable = False
        else:
            self.drawable = True

        # Calculates the width of each Node
        gap = int(width) // int(rows)
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                self.grid[i].append(Node(i,j,gap,rows,weight=weights))

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
                    if (self.drawable):
                        spot.draw(self.win)

    # Updates the neighbours of all the nodes in the Grid
    def update_neighbours(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbours(self.grid)

    # Draw the Grid to the pygame window
    def draw_grid(self):
        if self.drawable:
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
    def randomize(self, density=1):
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
        i = 0
        if density == 1:
        # Creates a random number of barriers
            for i in range(random.randrange(0,(self.rows*self.cols)//2)):
                blockade = (random.randrange(0,self.cols),random.randrange(0,self.rows))
                
                # Keep creating new coordinates until it is not the start or end
                while(blockade == start or blockade == end):
                    blockade = (random.randrange(0,self.cols),random.randrange(0,self.rows))
                self.grid[blockade[0]][blockade[1]].make_barrier()
        else:
            if density > 0.9:
                print("Invalid density value: Allowed values are 0-0.9, or default 1")
                return 
            # Create a copy of the grid so that values can be removed to help with the random generation of blockades
            available = []
            for i in range(self.rows):
                available.append([])
                for j in range(self.cols):
                    available[i].append(j)
            # remove the start and finish nodes
            available[start[0]].remove(start[1])
            available[end[0]].remove(end[1])

            for i in range(floor(self.rows*self.cols*density)):
                if len(available) == 1:
                    row_coord = 0
                else:
                    row_coord = random.randrange(0,len(available)-1)
                if len(available[row_coord]) == 1:
                    col_coord = 0
                else:
                    col_coord = random.randrange(0,len(available[row_coord])-1)
                col_coord = available[row_coord][col_coord]
                if len(available[row_coord]) == 1:
                    available.pop(row_coord)
                else:
                    available[row_coord].remove(col_coord)
                blockade = (row_coord, col_coord)
                # How to ensure that I can choose a unique Node in the graph each time while stil being pseudo random so as
                # to oppose long grid creation processing during high obstacle density 

                # Keep creating new coordinates until it is not the start or end
                while(blockade == start or blockade == end):
                    blockade = (random.randrange(0,self.cols),random.randrange(0,self.rows))
                self.grid[blockade[0]][blockade[1]].make_barrier()
            
        self.update_neighbours()
        return i

    # Writes the grid to a file
    def save_to_file(self, folderpath="Grids\\", description=''):
        number = 0
        if description == '':
            # Read the current number of Grids that have been written
            # in order to get a new filename

            with open("GridCreator\\GridNumber", 'r', newline='') as infile:
                number = int(infile.read())
            
            number += 1
            number = str(number)
            filename = "Grid_" + number
        else:
            filename = "Grid_" + description

        # Writes the grid to a file and adds surrounding barriers to the grid
        # because of this a 50x50 grid becomes a 52x52
        with open(folderpath+filename+".txt", "w") as outfile:
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
    
        with open(folderpath+filename+"_weights.txt", "w") as outfile:
            for i in range(self.rows+2):
                outfile.write('1 ')
            outfile.write('\n')
            for row in self.grid:
                outfile.write('1 ')
                for spot in row:
                    outfile.write(str(spot.weight)+' ')
                outfile.write('1\n')

            for i in range(self.rows+2):
                outfile.write('1 ')
        if description == '':
            with open("GridCreator\\GridNumber", 'w') as infile:
                infile.write(number)
        
        # Read a Grid from a file and save it to a Grid object
    # Maybe should be moved to a seperate class that handles creating all Grids
    @staticmethod
    def read_from_file(filepath):
        with open(filepath, "r") as map_file:
            # Obtaining Row Length
            row_test = map_file.readline()
            row_length = len(row_test) - 1
            # Reset File position
            map_file.seek(0)
            # Obtaining Total Rows
            length_test = map_file.read()
            rows = int(sqrt(len(length_test) - (row_length - 1)))
            map_file.seek(0)

            grid = Grid(None, rows, 0)
            obstacles = 0
            content = map_file.readlines()
            for row, line in enumerate(content):
                if row == rows:
                    break
                for col, value in enumerate(line):
                    if value == '0':
                        continue # Empty
                    elif value == '1':
                        grid.grid[col][row].make_barrier(); obstacles+=1 # Make Barrier
                    elif value == '2':
                        grid.grid[col][row].make_start() # Make Start
                        grid.start = grid.grid[col][row]
                    elif value == '3':
                        grid.grid[col][row].make_end() # Make End
                        grid.end = grid.grid[col][row]

            weight_map = map_file.name.strip(".txt")+"_weights.txt"

            if(exists(weight_map)):
                content_weight = open(weight_map,'r').readlines()
                for row, line in enumerate(content_weight):
                    if row == rows:
                        break
                    line = line.strip('\n')
                    weights = line.split(' ')
                    while('' in weights):
                        weights.remove('')
                    for col, weight in enumerate(weights):
                        grid.grid[col][row].weight = int(weight)
            else:
                for row in grid:
                    for spot in row:
                        spot.weight = 1
        grid.update_neighbours()
        return grid