import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import csv
from code.classes.protein import Protein
from code.algorithms.grid import Grid
from code.algorithms.random import Random

def visualize(lst):
    '''
    Visualizes the folded protein.
    '''
    print("LST:")
    print(lst)
    # coordinates = protein.solutions[0]
    coordinates = lst[1]
    print("COORDINATES:")
    print(coordinates)
    data = {"x":[], "y":[], "label":[]}

    # Append all amino acids + coordinates into the datafile to plot.
    for coord, label in coordinates.items():
        data["x"].append(coord[0])
        data["y"].append(coord[1])
        data["label"].append(label)

    print(data)

    # Plot figure of the grid
    plt.figure()
    plt.plot(data["x"], data["y"], '-ok')

    # Label all amino acids within the plot
    for x, y, label in zip(data["x"], data["y"], data["label"]):
        plt.annotate(label, xy = (x, y))

    plt.savefig("grid.png", format="png")


def hist(random):
    plt.figure()
    data = []
    
    for i in random.solutions:
        data.append(i[0])
    
    plt.hist(data)
    plt.savefig("hist.png", format="png")
    # As rendering voor wanneer negatieve waardes wel geprint kunnen worden.
    # plt.xlim(-5.5)
    # plt.ylim(-5,5)



