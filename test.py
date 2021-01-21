import csv
from code.classes.protein import Protein
from code.algorithms.random import Random
from code.visualisation.output import writecsv
from visualize import visualize, hist
from code.algorithms.depth_first import DepthFirst
from code.algorithms.hill_climber import HillClimber

# source = "data/testprotein.csv"
# protein = Protein(source, '3')
# randomfolder = Random()
# print(protein)
# randomfolder.run_random(protein, 1000)

# lst = randomfolder.get_best()
# print(lst)
# writecsv(protein, lst)
# visualize(lst)
# hist(randomfolder)

# data = []
# for i in protein.solutions:
#     data.append(i[0])
# plt.hist(data)

# lst = [1, 2, 3]
# lst.remove(4)
# print(lst)

# source = 'data/easyprotein.csv'
# protein_id = '4'
# protein = Protein(source, protein_id)
# hiker = HillClimber(protein)
# hiker.hike(10000, 5)
# best = hiker.get_best()
# hist(hiker)
# writecsv(protein, best)
# visualize(best)

source = 'data/testprotein.csv'
protein_id = '4'
protein = Protein(source, protein_id)
random = Random()
depth = DepthFirst(protein)
depth.run()
best = depth.best_solutions[0]
hist(depth)
writecsv(protein, best)

random.solutions = depth.solutions

visualize(best)