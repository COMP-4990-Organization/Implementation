
# Basic Imports

import pygame
import Constants as const

class Spot:

	# Constructor for Spot object

	def __init__(self, row, col, width, total_rows, grid):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = const.WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
		self.grid = grid

	# Function to reset node

	def reset(self):
		self.color = const.WHITE

	# All Getter Functions for Node

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == const.RED

	def is_open(self):
		return self.color == const.GREEN

	def is_barrier(self):
		return self.color == const.BLACK
	
	def is_start(self):
		return self.color == const.ORANGE

	def is_end(self):
		return self.color == const.TURQUOISE

	def is_path(self):
		return self.color == const.PURPLE

	# All Setter Functions for Node

	def make_start(self):
		self.color = const.ORANGE

	def make_closed(self):
		self.color = const.RED

	def make_open(self):
		self.color = const.GREEN

	def make_barrier(self):
		self.color = const.BLACK

	def make_end(self):
		self.color = const.TURQUOISE

	def make_path(self):
		self.color = const.PURPLE

    # All Helper Functions for Node

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
	
	def update_neighbors(self, grid):
		self.neighbors = []

		if self.row < self.total_rows - 1 and not self.grid[self.row + 1][self.col].is_barrier():	# Down
			self.neighbors.append(self.grid[self.row + 1][self.col])

		if self.row > 0 and not self.grid[self.row - 1][self.col].is_barrier():	# Up
			self.neighbors.append(self.grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not self.grid[self.row][self.col + 1].is_barrier():	# Right
			self.neighbors.append(self.grid[self.row][self.col + 1])

		if self.col > 0 and not self.grid[self.row][self.col - 1].is_barrier():	# Left
			self.neighbors.append(self.grid[self.row][self.col - 1])
	
	def __lt__(self, other):
		return False
