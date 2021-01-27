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

>>> pip install -r requirements.txt

## Usage

This is the input needed to run the program:

>>> python3 main.py source protein_id

To run the program with an example, call this in your terminal:

>>> python3 main.py data/hardprotein.csv 4

Next the program will ask you which algorithm you would like to run:

>>> Which algorithm do you want to run?
>>> r = random
>>> g = greedy
>>> h = hill climber
>>> p = hill climber (pull version)
>>> s = simulated annealing
>>> d = depth first

Choose an algorithm, for example random.

Then the program will ask how often you want to run the algorithm:

>>> How often do you want to run this algorithm?

For this example we choose 10,000 iterations.

When the program is finished running it will display the following:

>>> Algoritm took 6.44096565246582 seconds to run (without visualisation)

>>> The amount of solutions that were found with a specific stability score:
-19: 1
-18: 3
-17: 4
-16: 4
-15: 19
-14: 34
-13: 75
-12: 115
-11: 225
-10: 306
-9: 434
-8: 606
-7: 801
-6: 1152
-5: 1508
-4: 1633
-3: 1464
-2: 1031
-1: 470
0: 115r

>>> What title should I give the grid plot?

You then give the grid plot a name.

>>> What title should I give the bar plot?

Give the bar plot a name.

And finally:

>>> Program completed!

~ varies slightly per algorithm.

## Repository Structure

The following list describes the most important directories and files in the project, and where to find them:

* **/code**: holds all the code for this project.
* **/code/algorithms**: contains the code for the 5 algorithms: Random, Depth-First, Hill Climber, Hill Climber Pull, Greedy, Greedy Lookahead, Simulated Annealing and Simulated Annealing Pull.
* **/code/classes**: contains the 2 classes for this case: Protein and AminoAcid.
* **/code/visualisation**: contains output.py where the csv output files are created and where we can find the bar plot, bar.png, and the grid, grid.png. Contains visualize.py where we find the matplotlib code for the visualization. 

## The Algorithms

### Random



### Greedy and Greedy Lookahead

The Greedy algorithm is based on the random algorithm, except for the fact that the next folding is chosen greedily. The greedy choice is calculated by trying all possible folds for the next amino acids, and comparing the stability scores of the new configuration. The algorithm will choose randomly between foldings with the same stability score as outcome.

The Greedy Lookahead algorithm works a bit differently. For every amino acid, the best folding is calculated by placing the a sequence of the next X amount of amino acids at once, which is done through the Depth First algorithm. All retreived solutions are compared by stability scores, from which the solution with the highest stability score is taken. The first amino acid of the sequence used in the depth first algorithm, will save it's folding value. For the next amino acid, the process is repeated.

### Depth-first

The Depth First algorithm builds a stack of states of a protein with a unique folding for each state, and then searches the states for a best solution. It will take a 'parent' state from the stack and creates a new state, the 'child' state. This child state is where an amino acid has been added to the protein with a particular folding. It builds one child at a time until it has reached the end of the protein - where all amino acids have a folding. Once it has reached the end it checks the solution, then backtracks and builds a child with another folding possibility. It does this until it reaches the end once again and will continue to backtrack and build until it has searched the entire state space for the best solution.

### Hill Climber and Hill Climber Pull



### Simulated Annealing and Simulated Annealing Pull



## Authors

* Eva van der Heide
* Kaiden Sewradj 
* Wouter Vincken