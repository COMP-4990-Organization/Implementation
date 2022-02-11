
# Helper Imports
import Spot

class Grid:
    
    def __init__(self, rows, width, map_file_name):
        self.grid = []
        self.rows = rows
        self.width = width
        self.map_file_name = map_file_name
        pass

    def make_grid(self, rows, width, grid):
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot.Spot(i, j, gap, rows, grid)
                grid[i].append(spot)