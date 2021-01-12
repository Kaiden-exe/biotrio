import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import csv
from code.classes.protein import Protein
from code.algorithms.grid import Grid
from code.algorithms.random import Random

def visualize(grid):
    '''
    Visualizes the folded protein placed within the grid.
    '''
    # Turn different amino acids in corresponding colors
    # Empty(0): Purple, H(1): Green, P(2): Yellow

    # TODO
    # Indexatie fixen

    lstcount = 0
    for lst in grid:
        numbercount = 0
        for number in lst:
            if number == 'H':
                grid[lstcount][numbercount] = 1
            elif number == 'P':
                grid[lstcount][numbercount] = 2
            numbercount += 1
        lstcount += 1

    # TODO
    # Op de een of andere manier bonds visualiseren waardoor duidelijk wordt dat er bonds gevormd zijn tussen bepaalde aminozuren.

    # Plot figure of the grid
    print(grid)
    plt.figure()
    plt.matshow(grid)
    plt.savefig("grid.png", format="png")

    # As rendering voor wanneer negatieve waardes wel geprint kunnen worden.
    # plt.xlim(-5.5)
    # plt.ylim(-5,5)