from itertools import batched

#class Piece:
#    pass
    
'''
The piecemanager pieces together blocks, received from peers, back in to pieces. 
Once a piece has been fully assembled from individual blocks, it is verified using the sha1 hash from the metainfo file.
If the hash matches our piece, it is stored to disk.
'''

class PieceManager:

    #previously downloaded pieces of the data are stored somewhere, load them in
    def get_stored_pieces(self):
        pass
    

    def get_piece_length(self):
        return self.piece_length

    def __init__(self, parsed_metainfo_file):#piece_length):
        self.piece_length           = parsed_metainfo_file[b'info'][b'piece length']

        #converts byte hashes to strings, this can be used to verify pieces later
        _pieces                 = parsed_metainfo_file[b'info'][b'pieces']
        _pieces                 = [piece_hash for piece_hash in batched(_pieces, 20)]
        
        for index, piece_hash in enumerate(_pieces):
            _pieces[index] = ''.join(format(x, '02x') for x in piece_hash)
            
        #the hashes themselves should be in here
        self.pieces = _pieces
        #self.downloaded_pieces = [False for piece in self.pieces]

        self.outstanding_requests   = []
        self.data = self.get_stored_pieces()

    def add_block(self, block):
        print(f'piecemanager received block')
    
    def add_outstanding_request_for_piece(self, piece):
        self.outstanding_requests.append(piece)
    
    #if we don't have this piece already downloaded, and don't have a request outstanding for this piece, return true
    def misses_piece(self, piece):
        if piece not in self.pieces and piece not in self.outstanding_requests:
            return True
        return False
        
    #def has_missing_pieces(self):
    #return False in self.downloaded_pieces
