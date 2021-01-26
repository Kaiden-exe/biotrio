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

    # TODO - comment below: gain or get?
    # Gain data of the protein to visualize
    coordinates = lst[1]
    sorted_coordinates = sorted(coordinates.items(), key=lambda x: x[1].index)
    data = {"x":[], "y":[], "label":[]}

    # Append all amino acids + coordinates into the data file to plot
    for coord, label in sorted_coordinates:
        data["x"].append(coord[0])
        data["y"].append(coord[1])
        data["label"].append(label)

    # Plot figure of the grid
    plt.figure()
    ax = plt.gca()
    plt.plot(data["x"], data["y"], '-ok')

    # Set both the X- and Y-axis to integer values and label those
    plt.ylabel('Y-coordinates')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('X-coordinates')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Label all amino acids within the plot
    for x, y, label in zip(data["x"], data["y"], data["label"]):
        plt.annotate(label, xy = (x, y))

    # Give a title to the grid plot
    while True:
        name = input("What title should I give the grid plot?\n")
        try:
            name = str(name)
            break
        except ValueError:
            print("Please give a valid title (string).")
    
    plt.title(name)
    plt.savefig("grid.png", format="png")


def hist(algorithm, algor):
    # TODO - add docstring
    
    plt.figure()
    data = algorithm.solutions

    plt.hist(data)

    # Set both the X- and Y-axis to integer values and label those
    ax = plt.gca()

    # Set correct y-axis label for different algorithms
    if algor == 'd':
        plt.ylabel('Amount of solutions')
    else:
        plt.ylabel('Amount of iterations')

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('Stability score')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Give a title to the hist plot
    while True:
        name = input("What title should I give the hist plot?\n")
        try:
            name = str(name)
            break
        except ValueError:
            print("Please give a valid title (string).")
    
    plt.title(name)
    plt.savefig("hist.png", format="png")