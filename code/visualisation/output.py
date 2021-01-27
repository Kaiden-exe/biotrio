import csv

def get_folding(lst):
    '''
    Retreive all foldings from a best solution, used for csv output.
    '''
    positions = lst[1]
    pos_dict = dict(sorted(positions.items(), key=lambda x:x[1].index))
    folding_lst = []
    acid_lst = []

    for acid in pos_dict.values():
        folding_lst.append(acid.folding)
        acid_lst.append(acid.id)

    return [acid_lst, folding_lst]


def writecsv(protein, lst, source):
    '''
    Writes a csv file for a single protein. 
    '''
    score = lst[0]
    data = [[f"amino", "fold"]]
    lsts = get_folding(lst)
    acids = lsts[0]
    foldings = lsts[1]

    # Retrieve foldings of all amino acids in the protein
    for i in range(len(acids)):
        data.append([acids[i], foldings[i]])

    # Add score to data
    data.append(["score", score])

    # Output name generation
    source = source[:-len('.csv')]
    source = source[len('data/'):]
    name = f"{source}: {protein.id}"

    # Write the csv file
    with open(f"data/output/{name}", "w+", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)