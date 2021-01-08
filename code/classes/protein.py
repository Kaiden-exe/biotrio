from code.classes.aminoacid import AminoAcid

class Protein():
    def __init__(self, id, aminos):
        self.id = id
        self.aminoacids = self.load_acids(aminos)
        self.score = 0
        # key = (x, y), value = AminoAcid()
        self.positions = {}

    def load_acids(self, aminos):
        '''
        Converts the string of aminoacids into a list of chars,
        then returns a list of aminoacids accordingly.
        '''
        # protein = lijst van chars H/P
        protein = []
        protein[:0] = aminos
        acidlist = []
        index = 0
        for acid_id in protein:
            amino = AminoAcid(acid_id, index)
            acidlist.append(amino)
            index += 1
        return acidlist

    def add_position(self, acid, x, y):
        self.positions[(x, y)] = acid

    def __repr__(self):
        return f"{self.id}: f{self.aminoacids}"

