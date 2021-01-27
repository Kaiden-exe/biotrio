# Protein Pow(d)er by BioTrio

Proteins are long strands of amino acids that regulate many important processes in the human body. It is known that proteins are "folded" in the body cells, and that the specific folding determines their functioning. Misfolded proteins are at the basis of cancer, Alzheimer's and cystic fibrosis. It is therefore of great importance for both the pharmaceutical industry and medical science to be able to say something about the exact shape of the folding. In the protein structure: hydrophobic amino acids (H) like to be "next to each other", polar amino acids (P) do not have that preference. When two hydrophobic amino acids are next to each other, an "H-bond" is created due to the attractive forces between the two. And the more bonds, the more stable the protein. 

**The aim of this project** is to fold the proteins in such a way that the hydrophobic amino acids (H) found in the protein form cross-bonds - known as "H-bonds" - with one another. The more H-bonds the protein has the higher the stability of that protein. It is important for scientists and pharmacists to know to what stability of the protein could be folded at the maximum. The goal is to fold the given proteins in such a way that they are as stable as possible.

### Assumptions

* We assume a 2D grid in which we place every amino acid on a grid point. 
* The next amino acid is located on one of the adjacent grid points, allowing us to "fold" proteins down, with 90 degree angles.
* If two H's are next to each other on the grid, the total protein gets a -1 on the score. The lower the score, the more stable the protein.
* We go on to apply this to proteins that can have "C-bonds" too, which have a stronger bond of -5 making the protein even more stable.

## Requirements

All the code in this project is written entirely in Python 3.7. Requirements.txt contains all necessary packages to run the code successfully. These are easy to install via pip using the following instruction:

> pip install -r requirements.txt

## Usage

This is the input needed to run the program:

> python3 main.py source protein_id

To run the program with an example, call this in your terminal:

> python3 main.py data/easyprotein.csv 3

Next the program will ask you which algorithm you would like to run:

> Which algorithm do you want to run?
> r = random
> g = greedy
> h = hill climber
> p = hill climber (pull version)
> s = simulated annealing
> d = depth first

Choose an algorithm, for example random.

Then the program will ask how often you want to run the algorithm:

> How often do you want to run this algorithm?

For this example we choose 10,000 iterations.

When the program is finished running it will display the following:

> Algoritm took 0.7245039939880371 seconds to run (without visualisation)

> What title should I give the hist plot?

You then give the histogram plot a name.

> What title should I give the grid plot?

Give the grid plot a name.

And finally:

> Program completed!

## Repository Structure

The following list describes the most important directories and files in the project, and where to find them:

* **/code**: holds all the code for this project.
* **/code/algorithms**: contains the code for the 5 algorithms: Random, Depth-First, Hill Climber, Hill Climber Pull, Greedy, Greedy Lookahead, Simulated Annealing and Simulated Annealing Pull algorithms.
* **/code/classes**: contains the 2 classes for this case: Protein and AminoAcid.
* **/code/visualisation**: contains output.py where the csv output files are created and where we can find the hist.png and grid.png. Contains visualize.py where we find the matplotlib code for the visualization. 

## The Algorithms

### Random

### Greedy and Greedy Lookahead

### Depth-first

A Depth First algorithm that builds a stack of proteins with a unique folding for each instance.

### Hill Climber and Hill Climber Pull

### Simulated Annealing and Simulated Annealing Pull

## Authors

* Eva van der Heide
* Kaiden Sewradj 
* Wouter Vincken

## Problems 