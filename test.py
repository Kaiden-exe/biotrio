import csv
from code.classes.protein import Protein
from code.algorithms.random import Random
from code.visualisation.output import writecsv

source = "data/easyprotein.csv"
protein = Protein(source, '4')
randomfolder = Random()
randomfolder.fold_random(protein)
protein.set_stability()
writecsv(protein)