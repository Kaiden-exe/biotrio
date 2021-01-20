'''
Maak lege stack
Voeg eerste staat toe op stack
Herhaal tot stack leeg is:
    Paak bovenste staat op de stack
    Kies eerstvolgende node
    Als we een node hebben:
        Creer nieuwe staten voor elk mogelijke keuze voor node
    Anders:
        klaar?
'''
import copy
from .random import Random
from code.classes.protein import Protein
from code.classes.aminoacid import AminoAcid

class DepthFirst:
    """
    A Depth First algorithm that builds a stack of proteins with a unique folding for each instance.
    """
    def __init__(self, protein):
        self.protein = copy.deepcopy(protein)

        self.states = [copy.deepcopy(self.protein)]
        # self.index = 0

        # at the moment best_solution and best_stability are still single value
        self.best_solutions = []
        self.best_stability = 0


    def get_next_state(self):
        '''
        Method that gets the next state from the list of states.
        '''
        return self.states.pop()


    def build_children(self, new_protein, aminoacid):
        '''
        Creates all possible child-states and adds them to the list of states.
        '''
        # values are the possible foldings that we can assign to the amino acid
        # TODO
        # fold_list = Random.get_fold_list()
        # failsave for previous amino acid, surroundings acids

        # how do we check what folding the previous amino acid had (what folding the parent had)
        values = [-1, 1, -2, 2]

        # prev_fold = aminoacid.folding[]
        # values.remove(prev_fold)

        # we give the amino acid the different folding options that it can have
        for value in values:
            child = copy.deepcopy(new_protein)

            # assign the value to the amino acid's folding (using the aminoacid defined above)
            child.acid.folding = value
            child.depth_index += 1

            # add the child to the stack
            self.states.append(child)


    def check_solution(self, new_protein):
        '''
        Checks and accepts better solutions than the current solution.
        '''
        new_stability = new_protein.set_stability()
        if new_stability >= self.best_stability:

            # Save all best solutions, not only the last one found
            # Make sure to save in dictionary/list, with score + folding

            self.best_stability = new_stability
            self.best_solutions.append([self.best_stability, new_protein])


    def get_nofold_amino(self, new_protein):
        '''
        Returns the first amino acid with no folding.
        '''
        # where do I get the protein instance from??
        for amino in new_protein:
            if amino.folding is None:
                return amino
        
        return None

    
    def run(self, protein):
        '''
        Runs the algorithm untill all possible states are visited.
        '''
        # self.index = 0
        
        # while the stack is not empty
        while self.states:
            # we got a protein out of the states: the parent
            new_protein = self.get_next_state()

            # we look in our parent and we find the first amino acid without a folding
            # acid = new_protein.aminoacids[self.index]
            # self.index += 1

            aminoacid = self.get_nofold_amino(new_protein)
            
            # when there are no more foldings to do, remember what the stability score is
            # if acid == new_protein.aminoacids[-1]:
            #     acid.folding = 0
            if aminoacid is None:
                self.check_solution(new_protein)
            else:
                self.build_children(new_protein, aminoacid)
           
        print(f"New best solutions: {self.best_solutions}")

       
# see it as string.
# start with the first acid, fold and add to stack, go to the next one

# start with short string: which is the parent, which folding can it take, make those children, then go to a child and make that the new parent.
# in protein, find a way to 


# - Index
# - fold mogelijkheden  
# - coordinates
# leg de amino acid neer met een fold
# split op het strepje:
# (index, fold, coordinates) - (2, fold, (x, y)) 
# lengthe van de lijst na de splitter - do this check where you are in the protein
# to go from parent to child: overshcrijf wat er in de amino zuur zet, update de index,fold,coordinate.
# parent object aan het overshcrijven steeds. de protein word steeds langer, korter, langer, terug, andere tak af.
# een protein - heel veel strings die de protein representeren.
# als je een spegeling aan het maken bent - hou dat tegen door strings te vergelijken: prunen - throw away some of the branches.
# save the scores from the string - this branch is bad because it doing worse than the branch before.