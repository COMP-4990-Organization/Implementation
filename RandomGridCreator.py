# Creates random grids based on user input

# Basic Imports
import sys

# Import the necessary classes
from GridUtil.Grid import Grid

if __name__ == "__main__":

    # If the format of the input parameters are wrong, display an error message
    if(len(sys.argv) != 4):
        print("Error: Format should be python RandomGridCreator.py -num_of_grids -num_of_rows -num_of_cols")
        exit(0)
    
    # Create a grid, randomize it and save it
    grid = Grid(None, int(sys.argv[2]), 0, cols=int(sys.argv[3]))
    for i in range(int(sys.argv[1])):
        grid.randomize()
        grid.save_to_file()