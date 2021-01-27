# Protein Pow(d)er by BioTrio

Proteins are long strands of amino acids that regulate many important processes in the human body. It is known that proteins are "folded" in the body cells, and that the specific folding determines their functioning. Misfolded proteins are at the basis of cancer, Alzheimer's and cystic fibrosis. It is therefore of great importance for both the pharmaceutical industry and medical science to be able to say something about the exact shape of the folding. In the protein structure: hydrophobic amino acids (H) like to be "next to each other", polar amino acids (P) do not have that preference. When two hydrophobic amino acids are next to each other, an "H-bond" is created due to the attractive forces between the two. And the more bonds, the more stable the protein. 

**The aim of this project** is to fold the proteins in such a way that the hydrophobic amino acids (H) found in the protein form cross-bonds - known as "H-bonds" - with one another. The more H-bonds the protein has the higher the stability of that protein. It is important for scientists and pharmacists to know to what stability of the protein could be folded at the maximum. The goal is to fold the given proteins in such a way that they are as stable as possible.

*Description is based on the case description of Protein Pow(d)er provided by the Minor Programmeren of the University of Amsterdam.*

### Assumptions

* We simplify the problem to a 2D grid in which we place every amino acid on a grid point.
* The next amino acid is located on one of the adjacent grid points, allowing us to "fold" proteins with 90 degree angles.
* The folds are notated as 1 and -1 for folds along the X-axis, and as 2 and -2 for folds along the Y-axis.
* If two H's or an H and a C are on adjacent grid points, the total protein gets a -1 on the score. Two C's on adjacent grid points lowers the score with -5.

## Requirements

All the code in this project is written entirely in Python 3.7. Requirements.txt contains all necessary packages to run the code successfully. These are easy to install via pip (or pip3) using the following instruction:

```
pip3 install -r requirements.txt
```

## Usage

This program makes use of command-line arguments. This is the input needed to run the program:

```
python3 main.py source_file protein_id
```

To run the program **with an example**, call this in your terminal:

```
python3 main.py data/hardprotein.csv 4
```

Next the program will ask you which algorithm you would like to run:

```
Which algorithm do you want to run?
r = random
g = greedy
h = hill climber
p = hill climber (pull version)
s = simulated annealing
d = depth first
```
Choose an algorithm, for example **random**, **r**:

Then the program will ask how often you want to run the algorithm:

```
How often do you want to run this algorithm?
```

For this example we choose 10,000 iterations.

When the program is finished running it will display the following:

```
Algoritm took 6.44096565246582 seconds to run (without visualisation)
```

```
The amount of solutions that were found with a specific stability score:
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
0: 115
```

```
 What title should I give the grid plot?
```

You then give the grid plot a name.

```
What title should I give the bar plot?
```

Give the bar plot a name.

And finally:

```
Program completed!
```

##### The running of this program varies slightly per algorithm but the questions in the terminal will tell you what you need to input to get the results.


## Repository Structure

The following list describes the most important directories and files in the project, and where to find them:

* **/code**: holds all the code for this project.
* **/code/algorithms**: contains the code for the 8 algorithms: Random, Depth-First, Hill Climber, Hill Climber Pull, Greedy, Greedy Lookahead, Simulated Annealing and Simulated Annealing Pull.
* **/code/classes**: contains the 2 classes for this case: Protein and AminoAcid.
* **/code/visualisation**: contains output.py where the code for the csv output files are. Contains visualize.py where we find the matplotlib code for the visualization. 

The following list describes the data and results directories, and where to find them:

* **/data**: holds the output folder and the source files for this project: easyprotein.csv and hardprotein.csv.
* **/data/output**: contains the output files after running the program; the bar.png, grid.png and a .csv file that contains the amino acids, their foldings and the stability score.

## The Algorithms

The following are short descriptions of how each algorithm works.

### Random

The random algorithm will fold every amino acid in the given order randomly. If the protein folds onto itself, the algorithm will change the folding of the previous acid before folding the next amino acids. This way the algorithm makes sure it will always find a solution.

### Depth-first

The Depth First algorithm builds a stack of states of a protein with a unique folding for each state, and then searches the states for a best solution. It will take a 'parent' state from the stack and creates a new state, the 'child' state. This child state is where an amino acid has been added to the protein with a specific folding. It builds one child at a time until it has reached the end of the protein - where all amino acids in the protein are folded. Once it has reached the end of a branch in the search tree it saves the solution, then backtracks to another yet unfinished branch. This is done until it reaches the end once again and will continue to take states off the stack and build children until it has searched the entire state space for the best solution.

### Greedy and Greedy Lookahead

The Greedy algorithm is based on the random algorithm, except for the fact that the next folding is chosen greedily. The greedy choice is calculated by trying all possible folds for the next amino acids, and comparing the stability scores of the new configuration. The algorithm will choose randomly between foldings with the same stability score as outcome.

The Greedy Lookahead algorithm works a bit differently. For every amino acid, the best folding is calculated by placing the a sequence of the next X amount of amino acids at once, which is done through the Depth First algorithm. All retreived solutions are compared by stability scores, from which the solution with the highest stability score is taken. The first amino acid of the sequence used in the depth first algorithm, will save it's folding value. For the next amino acid, the process is repeated.

### Hill Climber and Hill Climber Pull

The Hill Climber algorithms both use the random algorithm to get a starting point. The regular Hill Climber moves a single amino acid (mutates) and does this an X amount of times per iteration. Better scores are always accepted, worse scores rejected and an equal score has a 50/50 chance of being accepted or rejected. 

The Hill Climber Pull mutates via a 'pull move', as defined by Lesh *et. al*, (2003). The 'pull move' picks an amino acid (i+1) and places the amino acid before that one (i) on a free space around it. If that breaks the amino acid chain, it will continue by placing the previous amino acid (i-1) on a parallel free space. If that does not repair the chain, the algorithm will keep pulling by placing amino acid j, on the original coordinates of amino acid j-2, until the chain is connected again. 

### Simulated Annealing and Simulated Annealing Pull

The regular Simulated Annealing algorithm works almost the same as the regular Hill Climber algorithm. The difference is the chance that a mutated protein with an equal or worse score is accepted. In the Hill Climber algorithm, worse scoring proteins always get rejected and equal scoring proteins have a 50/50 chance of being accepted. In the Simulated Annealing algoritm the chance that a worse or equal scoring protein gets accepted depends on the current simulated temperature. In the beginning the temperature is high and so the algorithm has a higher chance of accepting worse or equal scoring proteins. With each iteration, the temperature decreases, which in turn decreases the chance of a worse or equal scoring protein being accepted. The temperature decreases linearly.

The Simulated Annealing Pull algoritm works the same as the regular Simulated Annealing algorithm, except that it uses the Hill Climber Pull algorithm to make its mutations instead of using the regular Hill Climber algorithm.

## Authors

**Team BioTrio:**
* Eva van der Heide
* Kaiden Sewradj 
* Wouter Vincken

## References
Lesh, N., Mitzenmacher, M., & Whitesides, S. (2003). A complete and effective move set for simplified protein folding. *Proceedings of the Seventh Annual International Conference on Computational Molecular Biology - RECOMB ’03*, 1–13. <https://doi.org/10.1145/640075.640099>