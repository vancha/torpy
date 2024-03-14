class Piece:
    pass

class BlockManager:

    #previously downloaded pieces of the data are stored somewhere, load them in
    def get_stored_pieces(self):
        pass
    
    def get_piece_length(self):
        return self.piece_length

    def __init__(piece_length):
        self.piece_length = piece_length

        #or maybe call this self.pieces?
        self.data = self.get_stored_pieces()

    def add_block(self, block):
        pass

    def get_missing_pieces(self):
