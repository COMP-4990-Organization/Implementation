import sys
import time
import os

# Imports the other needed modules
# Assumes that the python module is being executed from the base 
# directory that the other sub-directories are in
directory = os.getcwd()
sys.path.insert(0,directory+'\GridCreator')
from Grid import Grid
from dijkstra import DIJKSTRA
from astar import ASTAR
from bfs import BFS
from dfs import DFS
from os.path import exists

import random

if __name__ == '__main__':
    SIZES = [50,100,500,1000,2500,5000,7500,10000]
    DENSITY = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    searches = [ASTAR(), DIJKSTRA(), BFS(), DFS()]
    open_option = 'w'

    # Would be best to change the name of the csv so that we don't write over each other's test
    # if exists('testing_out.csv'):
    #     open_option = 'a'

    # with open('Testing\\testing_out.csv', open_option) as outfile:
    #     outfile.write("SIZE, DENSITY, NUM_OF_BLOCKADES, SEARCH_ALGORITHM, NUM_OF_OPENED_NODES, LENGTH_OF_PATH, WEIGHT_OF_PATH, EXECUTION_TIME\n")
    #     for size in SIZES:
    #         grid = Grid(None, size, 0)
    #         for density in DENSITY:
    #             blockades = grid.randomize(density)
    #             grid.save_to_file('Testing\Test_Grids\\', 'Size,'+str(size)+'_Density,'+str(density))
    #             for search in searches:
    #                 start = time.perf_counter()
    #                 path, count = search.searchT(grid, grid.start, grid.end)
    #                 end = time.perf_counter()
    #                 current = grid.end
    #                 path_len = 0
    #                 weight = current.weight
    #                 while current in path:
    #                     current = path[current]
    #                     path_len += 1
    #                     weight += current.weight
    #                 outfile.write(str(size) + ', ' + str(density) + ', ' + str(blockades) + ', ' + str(search) + ', ' + str(count) + ', ' + str(path_len) + ', ' + str(weight) + ', ' + str(end-start) + '\n')
    #                 outfile.flush()

    grid = Grid.read_from_file(directory+'\Grids\Grid_Size,100_Density,0.3.txt')
    #blockades = grid.randomize(0.3)
    for search in searches:
        start = time.perf_counter()
        path, count = search.searchT(grid, grid.start, grid.end)
        end = time.perf_counter()
        current = grid.end
        path_len = 0
        weight = current.weight
        while current in path:
            current = path[current]
            path_len += 1
            weight += current.weight

        print(str(100) + ', ' + str(0.4) + ', ' + str(search) + ', ' + str(count) + ', ' + str(path_len) + ', ' + str(weight) + ', ' + str(end-start) + '\n')