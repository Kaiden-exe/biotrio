from .random import Random
from code.classes.protein import Protein, Temp_Protein
from random import choice, getrandbits, randint
from depth_first import DepthFirst
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
        self.solutions.append(score)


    def get_best(self):
        '''
        Returns a list of score and a dictionary of the best found folding.
        '''
        return [self.best.score, self.best.positions]


class HillClimber_Cut(HillClimber):
    def hike(self, iterations):
        '''
        Runs the alternative hill climber. 
        '''
        for i in range(iterations):
            new = copy.deepcopy(self.best)

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
        Makes a single mutation of mutations length. 
        '''
        
        # Get aminoacids to rearrange
        while True:
            temp_protein = self.get_aminoacids(protein)
            end_cor = self.get_end_coordinates(protein, temp_protein)
            depth_first = DepthFirst_Climber(temp_protein)
            depth_first.run()
            new_foldings = self.pick_solution(depth_first, end_cor)

            if len(new_foldings) > 0:
                break
            else:
                # TODO: Delete everything, before doing it all again
                # TODO: save the failed length etc.
                pass
            
    
    def get_aminoacids(self, protein):
        '''
        Returns a sub-string of aminoacids from the protein a temporary protein
        '''
        
        # Get a random chain length 
        protein_length = len(protein.aminoacids)
        min_length = 3
        max_length = int(protein_length / 4)
        if max_length < min_length:
            max_length = min_length
        chain_length = randin(min_length, max_length)


        last_option = protein_length - chain_length
        start = randint(0, last_option)
        aminoacids = protein.aminoacids[start:start + chain_length]
        
        return Temp_Protein(aminoacids)
        
    def get_end_coordinates(self, protein, temp_protein):
        '''
        Calculates and returns the coordinates the last aminoacid needs when the start is at (0,0).
        '''

        sorted_acids = protein.get_sorted_positions()
        start_index = temp_protein.aminoacids[0].index
        end_index = temp_protein.aminoacids[-1].index
        start_cor = sorted_acids[start_index][0]
        end_cor = sorted_acids[end_index][0]

        delta_x = end_cor[0] - start_cor[0]
        delta_y = end_cor[1] - start_cor[1]

        return (delta_x, delta_y)


    def pick_solution(self, depth_first, end_cor):
        '''
        Checks all solutions for a valid folding
        '''
        solutions = depth_first.solutions
        solutions.sort(key=lambda x:x[0], reverse=True)

        for solution in solutions:
            positions = solution[1].items()
            positions.sort(key=lambda x:x[1].index)
            
            if positions[-1][0] == end_cor:
                # TODO: check if acids are directly edited. If yes, you only have to change the coordinates
                return solutions[1].values()
        
        return []


class HillClimber_Pull(HillClimber):
    def __init__(protein):
        super().__init__(protein)
        self.success = 0

    def hike(self, iterations):
        '''
        Runs the hill climber algorithm.
        '''
        for i in range(iterations):
            new = copy.deepcopy(self.best)
            success = self.mutate(new)

            if success:
                self.success += 1
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

        # Pick random acid, but not the first
        i_plus = choice([i for i in protein.positions.items() if i[1] != protein.aminoacids[0]])
        i_plus_cor = i_plus[0]
        i = protein.aminoacids[i_plus[1].index - 1]
        sorted_acids = protein.get_sorted_positions()
        i_cor = sorted_acids[i.index][0]

        # Get free coordinates of i-1 and coordinates of i
        surrounding_coordinates = protein.get_surrounding_coordinates(i_plus[0][0], i_plus[0][1])
        free_coordinates = self.get_free_coordinates(protein, surrounding_coordinates)

        if free_coordinates == 0:
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
                    self.change_folding(protein, protein.aminoacid[i.index - 1], L)
                    return True
            else: 
                # Move i to L and i - 1 to C
                self.change_coordinates(protein, i, L)
                self.change_folding(protein, i, i_plus_cor)
<<<<<<< HEAD
            else: 
                for L in free_coordinates:
                    C = self.get_C(i_cor, i_plus_cor, L)

                    if C in protein.positions.keys():

                        if protein.positions[C] == protein.aminoacids[i.index - 1]:
                            self.change_coordinates(protein, i, L)
                            self.change_folding(protein, i, i_plus_cor)
                            self.change_folding(protein, protein.aminoacid[i.index - 1], L)
                            break
                    else: 
                        # TODO: C is free, move i to L and continue moving i - x until the new C is i - x - 1
                        # Move i to L and i - 1 to C
                        self.change_coordinates(protein, i, L)
                        i_min = protein.aminoacids[i.index - 1]
                        self.change_coordinates(protein, i_min, C)

                        # See if the previous amino acid is in the surrounding coordinates
                        prev = protein.aminoacids[i_min.index - 1]
                        next_cor = sorted_acids[i_min.index][0]
                        surrounding_coordinates = protein.get_surrounding_coordinates(i_min_cor[0], i_min_cor[1])
                        
                        # Keep moving amino acids until chain is back together 
                        # while not prev in surrounding_coordinates:
                        #     self.change_coordinates(protein, prev, next_cor)
                        #     prev = 
                        
=======
                i_min = protein.aminoacids[i.index - 1]
                self.change_coordinates(protein, i_min, C)
                self.change_folding(protein, i_min, i_cor)
>>>>>>> f77200d37653949290c1e156621bb9a62d5200bb

                # See if the previous amino acid is in the surrounding coordinates
                prev = protein.aminoacids[i_min.index - 1]
                surrounding_coordinates = protein.get_surrounding_coordinates(C[0], C[1])
                
                # If i - 2 not next to C, keep pulling until the chain is back together
                if not prev in surrounding_coordinates:
                    self.pull(protein, i, prev, surrounding_coordinates, sorted_acids)
     
                        
    def pull(self, protein, i, prev, surrounding_coordinates, original_positions):
        
        backwards_index = i.index

        # Keep pulling until the chain can be linked back together 
        while not prev in surrounding_coordinates:
            next_cor = sorted_acids[backwards_index][0]
            self.change_coordinates(protein, prev, next_cor)
            sorted_lst = protein.get_sorted_positions()
            next_acid_cor = sorted_lst[prev.index + 1][0]
            self.change_folding(protein, prev, next_acid_cor)
            prev = protein.aminoacids[prev.index - 1]
            surrounding_coordinates = protein.get_surrounding_coordinates(next_cor[0], next_cor[1])
            backwards_index -= 1
        
        # Change the fold of the final amino acid 
        self.change_folding(protein, prev, next_cor)
           

    def get_C(self, A, B, L):
        delta_x = L[0] - B[0]
        delta_y = L[1] - B[1]

        Cx = A[0] + delta_x
        Cy = A[0] + delta_y

        C = (Cx, Cy)

        return C

