import sys
import time
import os

# Imports the other needed modules
# Assumes that the python module is being executed from the base 
# directory that the other sub-directories are in
from GridUtil.Grid import Grid
from SearchAlgorithms.dijkstra import DIJKSTRA
from SearchAlgorithms.astar import ASTAR
from SearchAlgorithms.bfs import BFS
from SearchAlgorithms.dfs import DFS
from os.path import exists

import random

if __name__ == '__main__':
    SIZES = [50,100,500,1000,2500]
    DENSITY = [0.1,0.2,0.3,0.4]
    searches = [ASTAR(), DIJKSTRA(), BFS(), DFS()]
    open_option = 'w'

    # Comparing only Dijkstra's and BFS
    grid = Grid(None,100,0,weights=1)
    grid.randomize(0.1)
    start = time.perf_counter()
    path, count = searches[1].searchT(grid, grid.start, grid.end)
    end = time.perf_counter()
    current = grid.end
    path_len = 0
    weight = current.weight
    while current in path:
        current = path[current]
        path_len += 1
        weight += current.weight
    print('100, 0.1, Dijkstra, ' + str(count) + ', ' + str(path_len) + ', ' + str(weight) + ', ' + str(end-start) + '\n')
    grid.reset_search()
    start = time.perf_counter()
    path, count = searches[2].searchT(grid, grid.start, grid.end)
    end = time.perf_counter()
    current = grid.end
    path_len = 0
    weight = current.weight
    while current in path:
        current = path[current]
        path_len += 1
        weight += current.weight
    print('100, 0.1, BFS, ' + str(count) + ', ' + str(path_len) + ', ' + str(weight) + ', ' + str(end-start) + '\n')

    # Code used for testing different map sizes and densities
    # if exists('testing_out2.csv'):
    #     open_option = 'a'

    # with open('TestingMaterial\\gridcreation.csv', 'w') as timefile:
    #     with open('TestingMaterial\\testing_out2.csv', open_option) as outfile:
    #         timefile.write('SIZE, DENSITY, TIME_TO_CREATE\n')
    #         outfile.write("SIZE, DENSITY, NUM_OF_BLOCKADES, SEARCH_ALGORITHM, NUM_OF_OPENED_NODES, LENGTH_OF_PATH, WEIGHT_OF_PATH, EXECUTION_TIME\n")
    #         for size in SIZES:
    #             start = time.perf_counter()
    #             grid = Grid(None, size, 0)
    #             end = time.perf_counter()
    #             timefile.write(str(size)+', 0, '+str(end-start)+'\n')
    #             timefile.flush()
    #             for density in DENSITY:
    #                 start = time.perf_counter()
    #                 blockades = grid.randomize(density)
    #                 end = time.perf_counter()
    #                 timefile.write(str(size)+', '+str(density)+', '+str(end-start)+'\n')
    #                 timefile.flush()
    #                 grid.save_to_file('Grids2\\', 'Size,'+str(size)+'_Density,'+str(density))
    #                 for search in searches:
    #                     start = time.perf_counter()
    #                     path, count = search.searchT(grid, grid.start, grid.end)
    #                     end = time.perf_counter()
    #                     current = grid.end
    #                     path_len = 0
    #                     weight = current.weight
    #                     while current in path:
    #                         current = path[current]
    #                         path_len += 1
    #                         weight += current.weight
    #                     outfile.write(str(size) + ', ' + str(density) + ', ' + str(blockades) + ', ' + str(search) + ', ' + str(count) + ', ' + str(path_len) + ', ' + str(weight) + ', ' + str(end-start) + '\n')
    #                     outfile.flush()      
