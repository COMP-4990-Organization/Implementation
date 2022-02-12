from queue import Queue
import pygame

class BFS:

    def is_valid(self, spot, ROW):

        # Check if Spot is out of bounds
        if spot.row < 0 or spot.col < 0 or spot.row > ROW or spot.col > ROW:
            return False

        # Check if Spot is closed
        if spot.is_closed():
            return False

        # Check if Spot is barrier
        if spot.is_barrier():
            return False

        # All tests passed
        return True

    def bfs(self, draw, ROWS, grid, start):

        # Variables to help with gathering adjacent Spots

        dRow = [-1, 0, 1, 0]
        dCol = [0, 1, 0, -1]
        g_score = {(i,j): float("inf") for i in range(0,grid.rows) for j in range(0,grid.rows)}
        g_score[(start.row, start.col)] = 0

        # Adding start Spot to the spot_queue
        spot_queue = Queue()
        spot_queue.put(start)

        while not(spot_queue.empty()) > 0:
            # Setting the current spot to first item on the stack
            current_spot = spot_queue.get()

            # Checking if the current spot is valid
            if self.is_valid(current_spot, ROWS) == False:
                continue

            if current_spot.is_end():
                print("Total cost of the trip is " + str(g_score[(current_spot.row,current_spot.col)]))
                break

            current_spot.make_closed()

            for i in range(4):
                adjacentNodeRow = current_spot.row + dRow[i]
                adjacentNodeCol = current_spot.col + dCol[i]
                spot_queue.put(grid.grid[adjacentNodeRow][adjacentNodeCol])
                if self.is_valid(grid.grid[adjacentNodeRow][adjacentNodeCol], ROWS):
                    if not grid.grid[adjacentNodeRow][adjacentNodeCol].is_end():
                        grid.grid[adjacentNodeRow][adjacentNodeCol].make_open()
                    g_score[(adjacentNodeRow, adjacentNodeCol)] = g_score[(current_spot.row, current_spot.col)] + grid.grid[adjacentNodeRow][adjacentNodeCol].weight

            draw()