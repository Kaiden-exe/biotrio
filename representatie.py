##################################################
## The Contortionist 
##################################################
## This program calculates stability of randomly folded proteins.
##################################################
## Authors: Eva van der Heide, Kaiden Sewradj and Wouter Vincken
## License: unilicense 
## Version: 1.0.0
## Status: Done
##################################################

from code.algorithms.proteinfolding import fold_random, bonds
from code.algorithms.load_proteins import load_proteins
from code.visualisation.output import writecsv
from visualize import visualize

# Data wordt omgezet in lijst van eiwitten
source = "data/easyprotein.csv"
proteins = load_proteins(source)

# Elk eiwit wordt random gevouwen en stabiliteit wordt berekend
for protein in proteins:
    fold_random(protein)
    protein.score = bonds(protein)

# Folding en score worden in csv geschreven
for protein in proteins:
    writecsv(protein, f"{protein.id}")

# Voorlopige visualisation, met eigen source data
visualize()