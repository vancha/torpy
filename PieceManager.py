from Constants import SHA1_HASH_LENGTH

class Piece:
    def __init__(self, length, sha1_hash, index):
        self.blocks = []
        
        #hardcoded, bad!
        block_size = 16384#also the biggest possible value
        
        #because 16 blocks per piece should work?
        for i in range(length // block_size):
            self.blocks.append(Block(index, i * block_size, block_size, None))

        #this is the piece length in bytes
        self.length = length
        self.is_complete = False
    
    def matches_hash(self):
        pass
    
    def is_complete(self):
        for block in self.blocks:
            if not block.is_complete():
                return False
        return True
    
    def add_block(self, block):
        for existing_block in self.blocks:
            if existing_block.begin == block.begin:
                existing_block.block = block.block
                existing_block.is_complete = True
                break
                
        print('Couldnt find the block :( it got lost!')

#piece is made up of blocks
class Block:
    def __init__(self, index, begin, length, block=None):
        #zero based piece index
        self.is_requested   = False
        self.index          = index
        #zero based byte offset within piece
        self.begin          = begin
        self.length         = length
        #the block of data, the subset of the piece specified by the index
        self.block          = block
        if block:
            self.is_complete = True
        else:
            self.is_complete = False

    def from_message(message):
        return Block(message.index, message.begin, message.length, message.block)
        
    def is_complete(self):
        return self.is_complete()

    
'''
The piecemanager pieces together blocks, received from peers, back in to pieces. 
Once a piece has been fully assembled from individual blocks, it is verified using the sha1 hash from the metainfo file.
If the hash matches our piece, it is stored to disk.
'''

class PieceManager:

    #initializes an array of pieces, to keep track of which ones are already downloaded
    #should load the stored pieces from disk!
    def load_pieces(self, parsed_metainfo_file):
        pieces_data = parsed_metainfo_file[b"info"][b"pieces"]
        nr_of_pieces = len(pieces_data) // SHA1_HASH_LENGTH
        pieces = []
        for i in range(nr_of_pieces):
            piece_hash = pieces_data[i*20:i*20+20]
            pieces.append(Piece(parsed_metainfo_file[b'info'][b'piece length'], piece_hash, i))
        return pieces
        
    def __init__(self, parsed_metainfo_file):
        self.outstanding_requests   = []
        self.pieces                 = self.load_pieces(parsed_metainfo_file)
    
    def get_piece(self, piece_index):
        return self.pieces[piece_index]
        
    def update_pieces(self, block):
        self.pieces[block.index].add_block(block)
        
    def add_outstanding_request_for_piece(self, piece_index):
        self.outstanding_requests.append(piece_index)
    
    #if we don't have this piece already downloaded, and don't have a request outstanding for this piece, return true
    def misses_piece(self, piece_index):
        #print(f'piece manager misses piece at {piece_index}')
        if not self.pieces[piece_index].is_complete:
            print(f'piece manager misses piece at {piece_index}')
            return True
        else:
            print(f'piece manager does not miss piece at {piece_index}')
            return False
        
