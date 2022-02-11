
import pygame

class DFS:

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

    def dfs(self, draw, ROWS, grid, start):

        # Variables to help with gathering adjacent Spots

        dRow = [-1, 0, 1, 0]
        dCol = [0, 1, 0, -1]

        # Adding start Spot to the spot_stack
        spot_stack = []
        spot_stack.append(start)

        while len(spot_stack) > 0:
            # Setting the current spot to first item on the stack
            current_spot = spot_stack[len(spot_stack) - 1]

            # Popping the first Spot on the stack
            spot_stack.remove(spot_stack[len(spot_stack) - 1])

            # Checking if the current spot is valid
            if self.is_valid(current_spot, ROWS) == False:
                continue

            if current_spot.is_end():
                break

            current_spot.make_closed()

            for i in range(4):
                adjacentNodeRow = current_spot.row + dRow[i]
                adjacentNodeCol = current_spot.col + dCol[i]
                spot_stack.append(grid.grid[adjacentNodeRow][adjacentNodeCol])
                if self.is_valid(grid.grid[adjacentNodeRow][adjacentNodeCol], ROWS):
                    if not grid.grid[adjacentNodeRow][adjacentNodeCol].is_end():
                        grid.grid[adjacentNodeRow][adjacentNodeCol].make_open()

            draw()