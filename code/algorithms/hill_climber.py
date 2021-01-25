from .random import Random
from code.classes.protein import Protein
from random import choice, getrandbits
import copy

class HillClimber(Random):
    def __init__(self, protein):
        super().__init__()
        self.best = self.get_start(protein)

    def get_start(self, protein):
        '''
        Returns a randomly folded protein to start with.
        '''
        self.run_random(protein, 1)
        return protein
    
    def hike(self, iterations, mutations):
        '''
        Runs the hill climber algorithm.
        '''
        for i in range(iterations):
            new = copy.deepcopy(self.best)

            for j in range(mutations):
                self.mutate(new)

            new.set_stability()
            self.add_solution(new)

            if new.score < self.best.score:
                del self.best
                self.best = new
            elif new.score == self.best.score:
                if getrandbits(1):
                    del self.best
                    self.best = new
                else:
                    del new
            else:
                del new 
    
    def mutate(self, protein):
        '''
        Changes the coordinates of a single aminoacid.
        '''

        # New coordinates will be assigned to a random amino acid
        new_coordinates = ()
        while len(new_coordinates) < 2: 
            
            # Choose a random aminoacid from the protein and get all surronding coordinates (exclude last aminoacid)
            first_amino = protein.aminoacids[-1]
            while first_amino == protein.aminoacids[-1]:
                amino_coordinates = choice(list(protein.positions.keys()))
                first_amino = protein.positions[amino_coordinates]
            surrounding_coordinates = protein.get_surrounding_coordinates(amino_coordinates[0], amino_coordinates[1])
            
            # Add all coordinates that are unoccupied to a list
            free_coordinates = self.get_free_coordinates(protein, surrounding_coordinates)
            
            # Check if the any of the free coordinates is between the chosen aminoacid and two acids over
            if len(free_coordinates) > 0:
                try:
                    third_amino = protein.aminoacids[first_amino.index + 2]
                except IndexError: 
                   
                    #You can pick any for the last aminoacid
                    third_amino = None
                    new_coordinates = choice(free_coordinates) 
                    break
                
                # Check all free coordinates and see if any are adjacent to the third aminoacid
                for coordinates in free_coordinates:
                    new_coordinates = self.find_third_aminoacid(protein, third_amino, coordinates)
        
        # Change coordinates of second amino acid 
        second_amino = protein.aminoacids[first_amino.index + 1] 
        self.change_coordinates(protein, second_amino, new_coordinates)

        # Change foldings
        self.change_folding(protein, first_amino, new_coordinates)
        
        if third_amino:
            sorted_postitions = protein.get_sorted_positions()
            third_cor = sorted_postitions[third_amino.index][0]
            self.change_folding(protein, second_amino, third_cor)
        

    def get_free_coordinates(self, protein, surrounding_coordinates):
        '''
        Looks at the surrounding coordiates and returns a list of coordinates that are unoccupied.
        '''
        free_coordinates = []
        for coordinates in surrounding_coordinates:
            if coordinates not in protein.positions.keys():
                free_coordinates.append(coordinates)
        
        return free_coordinates

    
    def find_third_aminoacid(self, protein, third_amino, coordinates):
        '''
        Looks at coordinates and tries to find the third aminoacid in the surrounding coordinates.
        If third aminoacid is present, coordinates are returned. If not, then an empty tuple is returned.
        '''
        surrounding_coordinates = protein.get_surrounding_coordinates(coordinates[0], coordinates[1])
        for cor in surrounding_coordinates:
            try:
                amino = protein.positions[cor]
            except KeyError:
                amino = None

            if amino == third_amino:
                return coordinates
        
        return ()


    def change_coordinates(self, protein, aminoacid, coordinates):
        '''
        Changes the coordinates of an aminoacid to the given coordinates
        '''
        sorted_by_index = protein.get_sorted_positions()
        amino_cor = sorted_by_index[aminoacid.index][0]
        del protein.positions[amino_cor]
        protein.positions[coordinates] = aminoacid


    def change_folding(self, protein, aminoacid, next_coordinates):
        '''
        Cross-references the aminoacid and the coordinates of the next one to determine the folding
        '''

        # Get the aminoacid coordinates and the coordinates around it 
        lst = protein.get_sorted_positions()
        position = lst[aminoacid.index][0]
        surrounding_coordinates = protein.get_surrounding_coordinates(position[0], position[1])
        folds = Protein.get_fold_list(protein)

        # Find fold
        for i in range(len(surrounding_coordinates)):
            if surrounding_coordinates[i] == next_coordinates:
                folding = folds[i]
                break
        aminoacid.folding = folding

    def add_solution(self, protein):
        '''
        Add a solution to the list of solutions.
        '''
        score = protein.score
        copy_dict = copy.deepcopy(protein.positions)
        self.solutions.append([score, copy_dict])

    def get_best(self):
        '''
        Returns a list of score and a dictionary of the best found folding.
        '''
        return [self.best.score, self.best.positions]