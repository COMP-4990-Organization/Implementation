
# Basic Imports

import pygame
import math
import time
import sys

# Helper Imports

import Constants as const
import Grid

# Path Finding Algorithm Imports
from astar import ASTAR
from dfs import DFS

# Pygame Window Information

WIN = pygame.display.set_mode((const.WIDTH, const.WIDTH))
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
astar_object = ASTAR()
dfs_object = DFS()

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

# Drawing the grid to be displayed to the actor

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, const.GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, const.GREY, (j * gap, 0), (j * gap, width))

# Using the map file to generate the testing map

def upload_map(grid, rows):
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
	win.fill(const.WHITE)

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

	grid = Grid.Grid(ROWS, const.WIDTH, map_file_name)

	grid.make_grid(ROWS, const.WIDTH, grid.grid)
	
	start, end, obstacles = upload_map(grid.grid, ROWS)

	obstacle_density = (obstacles / map_size) * 100
	map_file.close()
	
	while True:
		draw(win, grid.grid, ROWS, width)
            
		if pygame.mouse.get_pressed()[0]: # LEFT
			pos = pygame.mouse.get_pos()
			row, col = get_clicked_pos(pos, ROWS, width)
			spot = grid.grid[row][col]

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
			spot = grid.grid[row][col]
			spot.reset()
			if spot == start:
				spot = end
			elif spot == end:
				end = None

		for row in grid.grid:
			for spot in row:
				spot.update_neighbors(grid)
		
		if algorithm_name == "astar":

			# Starting timer for execution of astar
			start_time = time.time()

			# Running Path Finding Algorithm
			astar_object.astar(lambda: draw(win, grid.grid, ROWS, width), heuristic, grid.grid, start, end)

			# Ending timer for execution of astar
			end_time = time.time()

			execution_time = end_time - start_time
			
		elif algorithm_name == "bfs":
			pass
		elif algorithm_name == "dfs":

			# Starting timer for execution of astar
			start_time = time.time()

			# Running Path Finding Algorithm
			dfs_object.dfs(lambda: draw(win, grid.grid, ROWS, width), ROWS, grid, start)

			# Ending timer for execution of astar
			end_time = time.time()

			execution_time = end_time - start_time

		elif algorithm_name == "dijkstra":
			pass
		else:
			print("Path Finding Algorithm not found. Valid Algorithms: astar, bfs, dfs, dijkstra")

		nodes_explored = count_nodes_explored(grid.grid, ROWS)

		print(algorithm_name)
		print(execution_time)
		print(map_size)
		print(obstacle_density)
		print(nodes_explored)

		quit(1)

# Running Program
main(WIN, const.WIDTH)