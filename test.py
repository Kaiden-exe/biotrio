import csv
from code.classes.protein import Protein
from code.algorithms.random import Random
from code.visualisation.output import writecsv
from visualize import visualize, hist

source = "data/testprotein.csv"
protein = Protein(source, '3')
randomfolder = Random()
print(protein)
randomfolder.run_random(protein, 1000)

lst = randomfolder.get_best()
print(lst)
writecsv(protein, lst)
visualize(lst)
hist(randomfolder)

# data = []
# for i in protein.solutions:
#     data.append(i[0])
# plt.hist(data)