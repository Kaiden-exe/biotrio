# Protein Pow(d)er by BioTrio

Proteins are long strands of amino acids that regulate many important processes in the human body. It is known that proteins are "folded" in the body cells, and that the specific folding determines their functioning; Misfolded proteins are at the basis of cancer, Alzheimer's disease and cystic fibrosis, among other things. It is therefore of great importance for both the pharmaceutical industry and medical science to be able to say something about the exact shape of the folding.

**The aim of this project** is to fold the proteins in such a way that the hydrophobic amino acids (H) found in the protein form cross-bonds - known as "H-bonds" - with one another. The more H-bonds the protein has the higher the stability of that protein. It is important for scientists and pharmacists to know to what stability of the protein could be folded at the maximum. The goal is to fold the given proteins in such a way that they are as stable as possible.

### Assumptions

* We assume a 2D grid in which we place every amino acid on a grid point. 
* The next amino acid is located on one of the adjacent grid points, allowing us to "fold" proteins down, with 90 degree angles.
* If two H's are next to each other on the grid, the total protein gets a -1 on the score. The lower the score, the more stable the protein.
* We go on to apply this to proteins that can have "C-bonds" too, which have a stronger bond of -5 making the protein even more stable.

## Installation Requirements

All the code for this project was been written in Python 3.7. To be able to run the project a few installations are required:
* Install matplotlib.

### matplotlib

> pip3 install matplotlib

~ if pip3 results in an error use pip.

## Usage

To run the program call:

> python3 main.py 

## Repository Structure

The following list describes the most important directories and files in the project, and where to find them:

* **/code**: holds all the code for this project.
* **/code/algorithms**: contains the code for the 5 algorithms: random, depth-first, hillclimber, greedy-combination and simulated annealing algorithms.
* **/code/classes**: contains the 2 classes for this case: Protein and AminoAcid.
* **/code/visualisation**: contains output.py that makes sure we get csv output files. Contains the matplotlib code for the visualization. 

## Authors

* Eva van der Heide
* Kaiden Sewradj 
* Wouter Vincken

#---------------------------------------------------------------------------------------------------->

Link: https://github.com/kaiden-exe/biotrio

Diary:

Thursday 7 Jan:
* Decide on the data structure: linear array.
* Started with the 1D in the form of a list, then went for 2D array.
* Decided on size of the 2D array per amino acid: n x n.
* Visualize grid in 2D array structure.
* Create classes for protein and amino acids.
* Make the random algorithm - hardcoded.
* Tests in test.py.
* Attempt to make an empty grid.
* Attempt to put a protein in the grid.
* Attempt made to make a visualization: mplot.py - problems with WSL connection to Ubuntu.

Friday 8 Jan:
* In the fold_random function: the protein no longer overlaps its own amino acids.
* fold_random: once the protein has folded the coordinates of the placed amino acid are saved.
* Adding stability function: set_stability.
* Complementing protein class to track folding sequence.
* Debugging issues with plotting our data.
* Starting a rewrite to turn out data into a dictionary, instead of a list of lists.
* In protein class: load_acids function - the positions attribute is no longer a list of lists but a dictionary:
* Coodinates are the keys, amino acids that are found on those coordinates are the value.
* Test this all in test.py: loop over all the proteins, fold the proteins, analyze the bonds between the amino acids.
* Representatie.py as an additional file to test the code.
* CSV function written in code/visualisation/output to create output files when running the code in representatie.py: creates a csv file, writes the header, makes a new row for each amino which contains the amino acid's id (H or P) and the folding, and as the footer places the stability score.
* Debugging to try and get the visualization to work - problems with negative folds and indexing.

Monday 11 Jan:
* Found out that our datastrucure was a mess - have too many loose functions out of place.

Tuesday 12 Jan:
* Started adjusting the datastructure in design.uxf. 
* Rearrange most functions to add them to the different classes.
* Got rid of protein_folding.py and put the function in the protein class.
* Random class and grid class added to the data struture.
* Added the run_random function to let our random algorithm run x number of times.
* Added a solutions attribute to the protein class.
* Cleaned the repository.
* Made sure the output files are saved in data/output folders instead of in the main repository.

Wednesday 13 Jan:
* Changed the visualization from a buggy figure to a scatter plot.
* Making sure we can give command-line arguments so that we can specifiy the source file.
* Debug the random_folding function to fix the problems in the folding.
* Visualization works! The random folding and the bonds between the neighboring amino acids can be seen.
* Make a graph to visualize the distribution of our scores.


