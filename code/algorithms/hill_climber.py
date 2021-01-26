from .random import Random
from code.classes.protein import Protein
from random import choice, getrandbits, randint
import copy

class HillClimber(Random):
    # TODO
    # add docstring
    def __init__(self, protein, runs):
        super().__init__()
        self.best = self.get_start(protein)
        self.iterations = runs


    def get_start(self, protein):
        '''
        Returns a randomly folded protein to start with.
        '''
        self.run_random(protein, 1)
        return protein
    

    def hike(self, mutations):
        '''
        Runs the hill climber algorithm.
        '''
        # TODO
        # maybe add a few comments
        for i in range(self.iterations):
            new = copy.deepcopy(self.best)

            for j in range(mutations):
                self.mutate(new)

            new.set_stability()
            self.add_solution(new)

            if new.score < self.best.score:
                del self.best
                self.best = new
            elif self.accept(new):
                del self.best
                self.best = new
            else:
                del new 

    
    def accept(self, new):
        print("wrong accept")
        if new.score == self.best.score and getrandbits(1):
            return True
        return False
    

    def mutate(self, protein):
        '''
        Changes the coordinates of a single aminoacid.
        '''
        # New coordinates will be assigned to a random amino acid
        new_coordinates = ()
        while len(new_coordinates) < 2: 
            
            # Choose a random amino acid from the protein and get all surronding coordinates (exclude last aminoacid)
            first_amino = protein.aminoacids[-1]
            while first_amino == protein.aminoacids[-1]:
                amino_coordinates = choice(list(protein.positions.keys()))
                first_amino = protein.positions[amino_coordinates]
            surrounding_coordinates = protein.get_surrounding_coordinates(amino_coordinates[0], amino_coordinates[1])
            
            # TODO - reword this comment
            # Add all coordinates that are unoccupied to a list
            free_coordinates = self.get_free_coordinates(protein, surrounding_coordinates)
            
            # TODO - reword this comment
            # Check if the any of the free coordinates is between the chosen amino acid and two acids over
            if len(free_coordinates) > 0:
                try:
                    third_amino = protein.aminoacids[first_amino.index + 2]
                except IndexError: 
                    
                    # TODO - pick any what?
                    # You can pick any for the last aminoacid
                    third_amino = None
                    new_coordinates = choice(free_coordinates) 
                    break
                
                # Check all free coordinates and see if any are adjacent to the third aminoacid
                for coordinates in free_coordinates:
                    new_coordinates = self.find_third_aminoacid(protein, third_amino, coordinates)
        
        # Change coordinates of second amino acid 
        second_amino = protein.aminoacids[first_amino.index + 1] 
        self.change_coordinates(protein, second_amino, new_coordinates)

        # TODO - change folding of the second amino acid?
        # Change foldings
        self.change_folding(protein, first_amino, new_coordinates)
        
        if third_amino:
            sorted_postitions = protein.get_sorted_positions()
            third_cor = sorted_postitions[third_amino.index][0]
            self.change_folding(protein, second_amino, third_cor)
        

    def get_free_coordinates(self, protein, surrounding_coordinates):
        '''
        Looks at the surrounding coordinates and returns a list of coordinates that are unoccupied.
        '''
        free_coordinates = []
        for coordinates in surrounding_coordinates:
            if coordinates not in protein.positions.keys():
                free_coordinates.append(coordinates)
        
        return free_coordinates

    
    def find_third_aminoacid(self, protein, third_amino, coordinates):
        '''
        Looks at coordinates and tries to find the third amino acid in the surrounding coordinates.
        If third amino acid is present, coordinates are returned. If not, then an empty tuple is returned.
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
        Changes the coordinates of an amino acid to the given coordinates.
        '''
        sorted_by_index = protein.get_sorted_positions()
        amino_cor = sorted_by_index[aminoacid.index][0]
        del protein.positions[amino_cor]
        protein.positions[coordinates] = aminoacid


    def change_folding(self, protein, aminoacid, next_coordinates):
        '''
        Cross-references the amino acid and the coordinates of the next one to determine the folding.
        '''
        # Get the amino acid coordinates and the coordinates around it 
        lst = protein.get_sorted_positions()
        position = lst[aminoacid.index][0]
        surrounding_coordinates = protein.get_surrounding_coordinates(position[0], position[1])
        folds = Protein.get_fold_list(protein)

        # TODO - maybe add more to this comment
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
        self.solutions.append(score)


    def get_best(self):
        '''
        Returns a list of score and a dictionary of the best found folding.
        '''
        return [self.best.score, self.best.positions]


class HillClimber_Pull(HillClimber):
    # TODO - add docstring

    def __init__(self, protein, runs):
        super().__init__(protein, runs)
        self.success = 0


    def hike(self):
        '''
        Runs the hill climber algorithm.
        '''

        for i in range(self.iterations):
            new = copy.deepcopy(self.best)
            success = self.mutate(new)

            if success:
                self.success += 1
                new.set_stability()
                self.add_solution(new)

                if new.score < self.best.score:
                    del self.best
                    self.best = new
                elif self.accept(new):
                    del self.best
                    self.best = new
                else:
                    del new 

        print(f"{self.success} out of {self.iterations} mutations were successful")


    def mutate(self, protein):
        # TODO - add docstring

        # Pick random amino acid, but not the first
        i_plus = choice([i for i in protein.positions.items() if i[1] != protein.aminoacids[0]])
        i_plus_cor = i_plus[0]
        i = protein.aminoacids[i_plus[1].index - 1]
        sorted_acids = protein.get_sorted_positions()
        i_cor = sorted_acids[i.index][0]

        # Get free coordinates of i-1 and coordinates of i
        surrounding_coordinates = protein.get_surrounding_coordinates(i_plus[0][0], i_plus[0][1])
        free_coordinates = self.get_free_coordinates(protein, surrounding_coordinates)

        if len(free_coordinates) == 0:
            return False

        # If i is the first amino acid, pull anywhere
        if i.index == 0:
            L = choice(free_coordinates)
            self.change_coordinates(protein, i, L)
            self.change_folding(protein, i, i_plus_cor)
            return True
         
        for L in free_coordinates:
            C = self.get_C(i_cor, i_plus_cor, L)

            if C in protein.positions.keys():

                # Move i to L 
                if protein.positions[C] == protein.aminoacids[i.index - 1]:
                    self.change_coordinates(protein, i, L)
                    self.change_folding(protein, i, i_plus_cor)
                    self.change_folding(protein, protein.aminoacids[i.index - 1], L)
                    return True
            else: 
                # Move i to L and i - 1 to C
                self.change_coordinates(protein, i, L)
                self.change_folding(protein, i, i_plus_cor)
                i_min = protein.aminoacids[i.index - 1]
                self.change_coordinates(protein, i_min, C)
                self.change_folding(protein, i_min, L)

                # See if the previous amino acid is in the surrounding coordinates
                prev = protein.aminoacids[i_min.index - 1]
                surrounding_acids = protein.get_surrounding_acids(C[0], C[1])

                # If i - 2 not next to C, keep pulling until the chain is back together
                if not prev in surrounding_acids:
                    self.pull(protein, i, prev, surrounding_acids, sorted_acids)


    def pull(self, protein, i, prev, surrounding_acids, original_positions):
        '''
        Keeps pulling until the chain can be linked back together or the last amino acid is reached.
        '''
        backwards_index = i.index

        while not prev in surrounding_acids and prev.index < backwards_index:
            next_cor = original_positions[backwards_index][0]
            self.change_coordinates(protein, prev, next_cor)
            sorted_lst = protein.get_sorted_positions()
            next_acid_cor = sorted_lst[prev.index + 1][0]
            self.change_folding(protein, prev, next_acid_cor)
            prev = protein.aminoacids[prev.index - 1]
            surrounding_acids = protein.get_surrounding_acids(next_cor[0], next_cor[1])
            backwards_index -= 1

        # Change the fold of the final amino acid
        if prev != protein.aminoacids[-1]:
            self.change_folding(protein, prev, next_cor)
           

    def get_C(self, A, B, L):
        '''
        Finds the fourth point (C) in the square ABL.
        '''
        delta_x = L[0] - B[0]
        delta_y = L[1] - B[1]
        Cx = A[0] + delta_x
        Cy = A[1] + delta_y
        C = (Cx, Cy)

        return C