# Stores the information needed to create a draw a Node

# Basic Imports
import pygame

# Import the necessary classes
from Constants import Constants

# Implementation of the Node class
class Node:

    # Initializer for the Node class
    # Takes the row and col of the Node, the width of the node
    # x and y offset and the total number of rows in the grid
    def __init__(self, row, col, width, x_offset, y_offset, total_rows):
        self.row = row
        self.col = col
        self.x = row * width + x_offset
        self.y = col * width + y_offset
        self.color = Constants.WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    # Basic Getters
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == Constants.RED
    
    def is_open(self):
        return self.color == Constants.GREEN

    def is_barrier(self):
        return self.color == Constants.BLACK

    def is_start(self):
        return self.color == Constants.ORANGE
    
    def is_end(self):
        return self.color == Constants.TURQUOISE

    def get_colour(self):
        return self.color

    # Basic Setters
    def reset(self):
        self.color = Constants.WHITE

    def make_closed(self):
        self.color = Constants.RED
    
    def make_open(self):
        self.color = Constants.GREEN

    def make_barrier(self):
        self.color = Constants.BLACK

    def make_start(self):
        self.color = Constants.ORANGE
    
    def make_end(self):
        self.color = Constants.TURQUOISE

    def make_path(self):
        self.color = Constants.PURPLE

    def set_colour(self, colour):
        self.color = colour

    # Draws the Node to the inputed pygame window
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Updates the neighbours of the Node
    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col  + 1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])