from code.algorithms.proteinfolding import random_folding

def create_grid(protein_length):
    '''
    Creates an empty grid, according to the initial length of the given protein.
    '''
    grids = [[0] * (protein_length*2+1) for _ in range(protein_length*2+1)]
    return grids

def fill_grid(protein):
    grid = create_grid(len(protein.aminoacids))
    position = 0
    
    for acid in protein.aminoacids:
        grid[0][position] = acid
        acid.index = position
        position += 1

# def fold_random(protein):
#     positionX = positionY = 0
#     protein.add_position(protein.aminoacids[0], positionX, positionY)
#     protein.aminoacids[0].folding = 1

#     # Het eiwit afmaken aan de hand van folding
#     for acid in protein.aminoacids[1:]:

#         while True:
#             folding = random_folding()
#             # Rotate amino acid over the X-axis
#             if folding == 1 or folding == -1:
#                 positionXb = positionX + folding

#             # Rotate amino acid over the Y-axis
#             else:
#                 positionYb = positionY + int(folding/2)
            
#             if not [positionXb, positionYb] in protein.positions.values():
#                 positionX = positionXb
#                 positionY = positionYb
#                 protein.add_position(acid, positionX, positionY)
#                 acid.folding = folding
#                 break


# def fill_grid_random(protein):
#     grid = create_grid(len(protein.aminoacids))
#     startpos = len(protein.aminoacids)
#     positionY = positionX = startpos
#     grid[positionY][positionX] = protein.aminoacids[0]
#     protein.aminoacids[0].folding = 1

#     # Het eiwit afmaken aan de hand van folding
#     index = 0
#     for acid in protein.aminoacids[1:]:

#         while True:
#             folding = random_folding()
#             # Rotate amino acid over the X-axis
#             if folding == 1 or folding == -1:
#                 positionXb = positionX + folding

#             # Rotate amino acid over the Y-axis
#             else:
#                 positionYb = positionY + int(folding/2)
            
#             if grid[positionYb][positionXb] == 0:
#                 positionY = positionYb
#                 positionX = positionXb
#                 grid[positionY][positionX] = acid
#                 protein.add_position(protein.aminoacids[index - 1], positionY, positionX)
#                 acid.folding = folding
#                 index += 1
#                 acid.index = index
#                 break