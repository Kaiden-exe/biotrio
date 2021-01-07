import csv
from code.classes.protein import Protein

def load_proteins(source):
    proteinlist = []
    with open(source, 'r') as data:
        reader = csv.reader(data)
        next(reader)
        for row in reader:
            proteinlist.append(Protein(row[0], row[1]))

    return proteinlist