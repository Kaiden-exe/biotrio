Link: https://github.com/kaiden-exe/biotrio

# biotrio
Protein Pow(d)er

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


INSTALL MATPLOTLIB USING PIP3 INSTALL MATPLOTLIB