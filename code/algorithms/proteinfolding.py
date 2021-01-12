from code.classes.aminoacid import AminoAcid
from code.classes.protein import Protein
import random

def random_folding():
    '''
    Returns a random folding value.
    '''
    foldList = [-1, 1, -2, 2]
    keuze = random.choice(foldList)
    return keuze


def fold_random(protein):
    protein.add_position(protein.aminoacids[0], positionX, positionY)
    protein.aminoacids[0].folding = 1
    positionXb = positionYb = 0

    # Finish the protein with random folding 
    for acid in protein.aminoacids[1:]:

        while True:
            folding = random_folding()
            
            # Rotate amino acid over the X-axis
            if folding == 1 or folding == -1:
                positionXb = positionX + folding

            # Rotate amino acid over the Y-axis
            else:
                positionYb = positionY + int(folding/2)
            
            # Assume position if X and Y coordinates are not already occupied by a previous acid
            if not [positionXb, positionYb] in protein.positions.values():
                positionX = positionXb
                positionY = positionYb
                protein.add_position(acid, positionX, positionY)
                acid.folding = folding
                break


def fold_choice():
    pass


def validate_fold():
    '''
    Checks if the current trie for folding is valid.
    '''
    pass


def bonds(protein):
    '''
    Analyses folded protein for H/H or H/C bonds and returns stability.
    '''
    coordinates = protein.positions.keys()
    stability = 0
    for x, y in coordinates:
        acid = protein.positions[(x, y)]
        if acid.id == 'H':
            surrounding = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            surrounding_aminos = []
            for coordinate in surrounding:
                try:
                    amino = protein.positions[coordinate]
                    surrounding_aminos.append(amino)
                except KeyError:
                    pass
                        
            for surround in surrounding_aminos:
                if not surround.index == acid.index + 1 or not surround.index == acid.index - 1:
                    if surround.id == 'H':
                        stability -= 1
                    # if surround.id == 'C':
                    # TODO 
    
    stability /= 2

    return stability

              