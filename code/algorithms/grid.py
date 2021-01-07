

def create_grid(protein_length):
    '''
    Creates an empty grid, according to the initial length of the given protein.
    '''
    grids = [[0] * (protein_length*2+1) for _ in range(protein_length*2+1)]
    return grids

    # i = 0
    # for grid in grids:
    #     print(grids[i])
    #     i =+ 1

def fill_grid(protein):
    grid = create_grid(len(protein.aminoacids))
    position = 0
    
    for acid in protein.aminoacids:
        grid[0][position] = protein.aminoacids[position]
        position += 1
        
def fill_grid_random(protein):
    grid = create_grid(len(protein.aminoacids))
    startpos = len(protein.aminoacids)
    positionY = positionX = startpos
    grid[positionY][positionX] = protein.aminoacids[0]
    protein.aminoacids[0].folding = 1

    # Het eiwit afmaken aan de hand van folding
    for acid in protein.aminoacids[1:]:

        while True:
        folding = random_folding()
        # Rotate amino acid over the X-axis
        if folding == 1 or folding == -1:
            positionX += folding

        # Rotate amino acid over the Y-axis
        else:
            positionY += int(folding/2)
        
        if grid[positionY][positionX] == 0:
            grid[positionY][positionX] = acid
            acid.folding = folding
            break