import csv

def custom_sort(x):
    # TODO - add docstring

    return x[1].index


def get_folding(lst):
    '''
    Retreive all foldings from a best solution, used for csv output.
    '''
    positions = lst[1]
    post = dict(sorted(positions.items(), key=custom_sort))
    folding_lst = []
    acid_lst = []

    for acid in post.values():
        folding_lst.append(acid.folding)
        acid_lst.append(acid.id)

    return [acid_lst, folding_lst]


def writecsv(protein, lst):
    '''
    Writes a csv file for a single protein. 
    '''
    score = lst[0]
    data = [[f"amino", "fold"]]
    lsts = get_folding(lst)
    acids = lsts[0]
    foldings = lsts[1]

    # TODO - maybe add a comment?
    for i in range(len(acids)):
        data.append([acids[i], foldings[i]])
    data.append(["score", score])
    name = f"Protein: {protein.id}"

    # TODO - maybe add a comment?
    with open(f"data/output/{name}", "w+", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)