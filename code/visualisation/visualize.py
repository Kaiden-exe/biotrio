import matplotlib
matplotlib.use('Agg')

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator
from code.classes.protein import Protein
from code.algorithms.randomize import Random

def solution_count(algorithm):
    '''
    Show the amount of each stability score that is found.
    '''
    print("The amount of solutions that were found with a specific stability score:")
    for key in sorted(algorithm.sol_dict):
        print(f"{key}: {algorithm.sol_dict[key]}")


def visualize(lst):
    '''
    Visualizes the folded protein.
    '''
    data = {"x":[], "y":[], "label":[]}
    
    # Retreive data of the protein to visualize
    coordinates = lst[1]
    sorted_coordinates = sorted(coordinates.items(), key=lambda x: x[1].index)

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


def bar(algorithm, algor):
    '''
    Plot solutions of the used algorithm in a histogram.
    '''
    # Plot all stability scores and the amount of times they have been found
    plt.figure()
    plt.bar(list(algorithm.sol_dict.keys()), algorithm.sol_dict.values(), color='b')

    # Set both the X- and Y-axis to integer values and label those
    ax = plt.gca()

    # Create lists of all labels and values for the X-axis
    x_labels = []
    all_scores = []
    for key in algorithm.sol_dict:  
        x_labels.append(key)
        all_scores.append(key)

    ax.set_xticks(all_scores)
    plt.xlabel('Stability score')

    # Set correct Y-axis label for different algorithms
    if algor == 'd':
        plt.ylabel('Amount of solutions')
    else:
        plt.ylabel('Amount of iterations')

    # Make the values on the Y-axis integers only
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Give a title to the bar plot
    while True:
        name = input("What title should I give the bar plot?\n")
        try:
            name = str(name)
            break
        except ValueError:
            print("Please give a valid title (string).")
    
    plt.title(name)
    plt.savefig("data/output/bar.png", format="png")