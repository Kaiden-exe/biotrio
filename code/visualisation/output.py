import csv

def writecsv(protein, name):
    data = [[f"amino: {protein.id}", "fold"]]
    for acid in protein.aminoacids:
        data.append([acid.id, acid.folding])
    data.append(["score", protein.score])
    with open(f"{name}", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    