import csv

def writecsv(protein):
    '''
    Writes a csv file for a single protein. 
    '''
    # TODO
    ## VOlgens mij slaat de titel nergens op op dit moment.
    data = [[f"Protein: {protein.id}", "fold"]]
    for acid in protein.aminoacids:
        data.append([acid.id, acid.folding])
    data.append(["score", protein.score])
    name = f"Protein: {protein.id}"
    with open(f"data/output/{name}", "w+", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    


    

  