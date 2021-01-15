from .random import Random
from random import choice
import copy

class HillClimber(Random):
    def __init__(self, protein):
        super().__init__()
        self.best = self.get_start(protein)

    def get_start(self, protein):
        self.run_random(protein, 1)
        return protein
    
    def hike(self, iterations):
        '''
        Runs the hill climber algorithm.
        '''
        for i in range(iterations):
            new = copy.deepcopy(self.best)
            self.mutate(new)
            self.add_solution(new)

            if new.score < self.best.score:
                del self.best
                self.best = new
            else:
                del new
    
    def mutate(self, protein):
        '''
        Changes the coordinates of a single aminoacid.
        '''

        # New coordinates will be assigned to a random amino acid
        new_coordinates = None
        while len(new_coordinates) < 2:
            
            # Choose a random aminoacid from the protein and get all surronding coordinates (exclude last aminoacid)
            first_amino = protein.aminoacids[-1]
            while first_amino == protein.aminoacids[-1]:
                amino_coordinates = choice(list(protein.positions.keys()))
                first_amino = protein.positions[amino_coordinates]
            surrounding_coordinates = protein.get_surrounding_coordinates(amino_coordinates[0], amino_coordinates[1])
            
            # Add all coordinates that are unoccupied to a list
            free_coordinates = []
            for coordinates in surrounding_coordinates:
                if coordinates not in protein.positions.keys():
                    free_coordinates.append(coordinates)
            
            # Check if the any of the free coordinates is between the chosen aminoacid and two acids over
            if len(free_coordinates) > 0:
                try:
                    third_amino = protein.aminoacids[first_amino.index + 2]
                except IndexError: 
                    third_amino = None
                    new_coordinates = choice(free_coordinates) #You can pick any for the last aminoacid
                    break

                # TODO: add break somewhere for when you have found new coordinates 
                for coordinates in free_coordinates:
                    surround = protein.get_surrounding_coordinates(coordinates[0], coordinates[1])
                    for cor in surround:
                        try:
                            amino = protein.positions[cor]
                        except ValueError:
                            amino = None

                        if amino == third_amino:
                            new_coordinates = coordinates
        
        # Change coordinates of amino acid 
        second_amino = protein.aminoacids[first_amino.index + 1]   
        lst = protein.positions.items()
        sorted_by_index = sorted(lst, key=lambda x: x[1].index)
        second_amino_cor = sorted_by_index[second_amino.index][0]
        del protein.positions[second_amino_cor]
        protein.positions[new_coordinates] = second_amino

        # Change folding of first amino 
        folds = self.get_fold_list()
        for i in range(len(surrounding_coordinates)):
            if surrounding_coordinates[i] == new_coordinates:
                folding = folds[i]
                break
        first_amino.folding = folding

        # Change folding of second amino if there is a third one
        if third_amino:
            third_amino_cor = sorted_by_index[third_amino.index][0]
            surrounding_coordinates = protein.get_surrounding_coordinates(new_coordinates[0], new_coordinates[1])
            for i in range(len(surrounding_coordinates)):
            if surrounding_coordinates[i] == third_amino_cor:
                folding = folds[i]
                break
        second_amino.folding = folding

    def add_solution(self, protein):
        '''
        Add a solution to the list of solutions.
        '''
        copy_score = copy.deepcopy(protein.score)
        copy_dict = copy.deepcopy(protein.positions)
        self.solutions.append([copy_score, copy_dict])