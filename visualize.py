import matplotlib
matplotlib.use('Agg')

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator
from code.classes.protein import Protein
from code.algorithms.random import Random

def visualize(lst):
    '''
    Visualizes the folded protein.
    '''
    # Gain data of the protein to visualize
    coordinates = lst[1]
    sorted_coordinates = sorted(coordinates.items(), key=lambda x: x[1].index)
    data = {"x":[], "y":[], "label":[]}

    # Append all amino acids + coordinates into the datafile to plot.
    for coord, label in sorted_coordinates:
        data["x"].append(coord[0])
        data["y"].append(coord[1])
        data["label"].append(label)

    # Plot figure of the grid
    plt.figure()
    ax = plt.gca()
    plt.plot(data["x"], data["y"], '-ok')

    # Set both the X- and Y-axis to integer values
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

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



