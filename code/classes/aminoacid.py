class AminoAcid():
    def __init__(self, id):
        self.id = id
        self.folding = None

    def __repr__(self):
        return f"{self.id}"