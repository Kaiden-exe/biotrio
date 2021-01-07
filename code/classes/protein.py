from .aminoacid import AminoAcid

class Protein():
    def __init__(self, id, aminos):
        self.id = id
        self.aminoacids = self.load_acids(aminos)
        self.score = 0

    def load_acids(self, aminos):
        '''
        Converts the string of aminoacids into a list of chars,
        then returns a list of aminoacids accordingly.
        '''
        protein = []
        protein[:0] = aminos
        acidlist = []
        for sequence in protein:
            acidlist.append(AminoAcid(sequence))
        return acidlist

    def __repr__(self):
        return f"{self.id}"

