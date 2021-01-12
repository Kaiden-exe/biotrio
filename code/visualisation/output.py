import csv

def writecsv(protein, name):
    '''
    Writes a csv file for a single protein. 
    '''
    # TODO
    ## VOlgens mij slaat de titel nergens op op dit moment.
    data = [[f"amino: {protein.id}", "fold"]]
    for acid in protein.aminoacids:
        data.append([acid.id, acid.folding])
    data.append(["score", protein.score])
    with open(f"{name}", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    