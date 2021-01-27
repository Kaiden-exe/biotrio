import matplotlib
matplotlib.use('Agg')

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator
from code.classes.protein import Protein
from code.algorithms.randomize import Random

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
    plt.savefig("data/output/grid.png", format="png")


def hist(algorithm, algor):
    '''
    Plot solutions of the used algorithm in a histogram.
    '''
    dictonary = algorithm.sol_dict
    new_dictonary = {str((k)):v1 for k, v in dictonary.items() for v1 in v.items()}
    # new_dictonary = {str((k,k1)):v1 for k, v in dictonary.items() for k1,v1 in v.items()}
    plt.figure()
    plt.bar(new_dictonary.keys(), new_dictonary.values(), width=.5, color='g')
    plt.savefig("data/output/hist.png", format="png")
    
    # TODO --------------------------------------------------- Eigen functie?
    # Show the amount of each stability score that is found
    for key in sorted(algorithm.sol_dict):
        print(f"{key}: {algorithm.sol_dict[key]}")
    
    ###################################################
    data = []
    for i in algorithm.solutions:
        data.append(i)
    ###################################################
    plt.figure()
    plt.hist(algorithm.sol_dict)

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
    plt.savefig("data/output/hist.png", format="png")