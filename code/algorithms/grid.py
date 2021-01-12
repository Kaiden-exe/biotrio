from code.algorithms.random import Random

class Grid():
    '''
    The grid class can be used to visualize the specific folding of a protein.
    '''
    def __init__(self, protein):
        self.protein = protein
        self.protein_length = len(protein.aminoacids)
        self.grid = self.create_grid(self.protein_length)

    def create_grid(self, protein_length):
        '''
        Creates an empty grid, according to the initial length of the given protein.
        '''
        grids = [[0] * (protein_length*2+1) for _ in range(protein_length*2+1)]
        return grids

    def fill_grid(self, protein):
        '''
        Fill the grid with a corresponding protein.
        '''
        grid = self.create_grid(len(protein.aminoacids))
        position = 0
        
        for acid in protein.aminoacids:
            grid[0][position] = acid
            acid.index = position
            position += 1

        '''
        ---> Loop door protein_dict heen en tel de lengte van de protein + 1 bij elke x en y waarde van elke key op.
        Hierdoor komt het 0-punt niet linksbovenin / rechtsonderin maar exact in het midden van de grid.
        Op deze manier zijn negatieve waarde niet negatief, maar wel ten opzichte van het nulpunt.
        '''