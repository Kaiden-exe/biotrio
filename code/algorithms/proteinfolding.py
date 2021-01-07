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

def fold_choice():
    pass

def validate_fold():
    pass