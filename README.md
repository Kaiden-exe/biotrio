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
* The protein no longer overlaps its own amino acids.
* Once the protein has folded the coordinates of the placed amino acid are saved.
* Adding stability function: bonds.
* Complementing protein class to track folding sequence.
* Debugging issues with plotting our data.
* Starting a rewrite to turn out data into a dictionary, instead of a list of lists.
* So in the protein class, under the load_acids function, the positions attribute is no longer a list of lists but a dictionary:
* Coodinates are the keys, amino acids that are found on those coordinates are the value.
* Make sure the bonds function gets all the coordinates of the amino acids.
* Check that the amino acid is an 'H', so that it can form bonds.
* Make a list of all the amino acids that are found on the coordinates that surround the amino acid in question.
* Check whether the coordinates are already in the dictionary, means thatthere is an amino acid present.
* Then add it to the list of amino acids that surround the amino acid in question.
* Check whether the index of the amino acid that is surrounding our amino acid in question is not the next amino acid in the sequence of the protein - where no bonds can form.
* Check that it is an H, if it is then take one off of the stability score, divide it by 2, then return the stability.
* Test this all in test.py: loop over all the proteins, fold the proteins, analyze the bonds between the amino acids.
* Write a csv function to get the output: creates the header, makes a new row for each amino which contains the amino acid's id (H or P) and the folding and as last the stability score.

Monday 11 Jan:
* 