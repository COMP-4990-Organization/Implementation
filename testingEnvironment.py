
# Basic Imports

import pygame
import math
import time
import sys

# Helper Imports

# import sqlHelper

# Path Finding Algorithm Imports

import astar

# Pygame Window Information

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Capstone Project")

# --------------- Environment Helper Functions --------------- #

def execution_check():
	
	'''
	Description: This function checks if the user has entered the right amount 
				 of arguments. Also this will return key information, which testing map 
				 to use and what algorithm to run on the map.
	'''

	if len(sys.argv) == 3:
		map_file_name = sys.argv[1]				# Map File Name
		algorithm_name = sys.argv[2].lower()	# Algorithm Name
	else:
		print("Run Template: python testingEnvironment.py map-file algorithm-name ")
		exit(0)

	return map_file_name, algorithm_name

# Command Line Arguments

map_file_name, algorithm_name = execution_check()

# Path Finding Objects

map_file = open(map_file_name, "r")
astar_object = astar.ASTAR()

# All Used Colours

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:

	# Constructor for Spot object

	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	# Function to reset node

	def reset(self):
		self.color = WHITE

	# All Getter Functions for Node

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK
	
	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def is_path(self):
		return self.color == PURPLE

	# All Setter Functions for Node

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

    # All Helper Functions for Node

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
	
	def update_neighbors(self, grid):
		self.neighbors = []

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():	# Down
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():	# Up
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():	# Right
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():	# Left
			self.neighbors.append(grid[self.row][self.col - 1])
	
	def __lt__(self, other):
		return False

# --------------- Path Finding Algorithm Helper Functions --------------- #

# Solution Visualization Function

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

# Heuristic Function

def heuristic(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# Explored Node Function

def count_nodes_explored(grid, rows):
	nodes_explored = 0
	for i in range(rows):
		for j in range(rows):
			if grid[i][j].is_closed() or grid[i][j].is_path():
				nodes_explored += 1
	return nodes_explored

# --------------- Generating Testing Environment Functions --------------- #

# Filling grid object with spot objects

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)
	
	return grid

# Drawing the grid to be displayed to the actor

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Using the map file to generate the testing map

def generate_map(grid, rows):
    start = None; end = None; obstacles = 0
    content = map_file.readlines()
    for row, line in enumerate(content):
        if row == rows:
            break
        for col, value in enumerate(line):
            if value == '0':
                continue # Empty
            elif value == '1':
                grid[col][row].make_barrier(); obstacles+=1 # Make Barrier
            elif value == '2':
                grid[col][row].make_start() # Make Start
                start = grid[col][row]
            elif value == '3':
                grid[col][row].make_end() # Make End
                end = grid[col][row]
    return start, end, obstacles

# Main draw function of the program will refresh every frame

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

# Mouse Event Information Function (Get position of mouse click)

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

# --------------- Driver Function --------------- #

def main(win, width):
	
	# Obtaining Row Length

	map_file = open(map_file_name, "r")
	row_test = map_file.readline()
	row_length = len(row_test) - 1
	map_file.close()
	
	# Obtaining Total Rows

	map_file = open(map_file_name, "r")
	length_test = map_file.read()
	ROWS = int(math.sqrt(len(length_test) - (row_length - 1)))

	map_size = ROWS ** 2
	
	grid = make_grid(ROWS, width)
	start, end, obstacles = generate_map(grid, ROWS)

	obstacle_density = (obstacles / map_size) * 100
	map_file.close()
	
	while True:
		draw(win, grid, ROWS, width)
            
		if pygame.mouse.get_pressed()[0]: # LEFT
			pos = pygame.mouse.get_pos()
			row, col = get_clicked_pos(pos, ROWS, width)
			spot = grid[row][col]

			if not start and spot != end:
				start = spot
				start.make_start()

			elif not end and spot != start:
				end = spot
				end.make_end()

			elif spot != end and spot != start:
				spot.make_barrier()
		
		elif pygame.mouse.get_pressed()[2]: # RIGHT
			pos = pygame.mouse.get_pos()
			row, col = get_clicked_pos(pos, ROWS, width)
			spot = grid[row][col]
			spot.reset()
			if spot == start:
				spot = end
			elif spot == end:
				end = None

		for row in grid:
			for spot in row:
				spot.update_neighbors(grid)
		
		if algorithm_name == "astar":

			# Starting timer for execution of astar

			start_time = time.time()

			# Running Path Finding Algorithm
			astar_object.astar(lambda: draw(win, grid, ROWS, width), heuristic, reconstruct_path, grid, start, end)

			# Ending timer for execution of astar
			end_time = time.time()

			execution_time = end_time - start_time
			
		elif algorithm_name == "bfs":
			pass
		elif algorithm_name == "dfs":
			pass
		elif algorithm_name == "dijkstra":
			pass
		else:
			print("Path Finding Algorithm not found. Valid Algorithms: astar, bfs, dfs, dijkstra")

		nodes_explored = count_nodes_explored(grid, ROWS)

		print(algorithm_name)
		print(execution_time)
		print(map_size)
		print(obstacle_density)
		print(nodes_explored)

		quit(1)

# Running Program
main(WIN, WIDTH)