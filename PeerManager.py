from PieceManager import PieceManager
from Peer import Peer
from Tracker import Tracker
import Constants
import time


'''
The PeerManager can generate peer connections based on the tracker response. 
It tries to keep a buch of peers downloading, and kills the peers which are no longer active. can request more peers from the tracker.
Also occasionally checks if peers have downloaded new blocks, and if so, adds them to the piecemanager.
'''

class PeerManager:
    def __init__(self, tracker_response, parsed_metainfo_file):
        self.piece_manager = PieceManager(parsed_metainfo_file)
        self.peer_list = [Peer(peer[b'ip'].decode('utf-8'), peer[b'peer id'], peer[b'port'], parsed_metainfo_file ) for peer in tracker_response[b'peers']]
        self.run()
        
    #useful if you want to know if we are still downloading
    def has_active_peers(self):
        for peer in self.peer_list:
            if peer.is_active:
                return True
        return False

    #used for cleanup, it's no use to have inactive peers taking up memory
    def has_inactive_peers(self):
        for peer in self.peer_list:
            if not peer.is_active:
                return True
        return False
    
    #the actual cleanup
    def remove_inactive_peers(self):
        for peer in self.peer_list:
            if not peer.is_active:
                peer.quit()
                self.peer_list.remove(peer)
    
    #the infinite loop that performs management of peers: keeping the number of peers up, removing inactive peers, adding peer pieces to piecemanager
    def run(self):
        try:
            while True:
                if self.has_inactive_peers():
                    self.remove_inactive_peers()
                
                for peer in self.peer_list:
                    for piece_index in peer.available_pieces:
                        if self.piece_manager.misses_piece(piece_index):
                            self.piece_manager.add_outstanding_request_for_piece(piece_index)
                            peer.queue_block_requests(self.piece_manager.get_piece(piece_index).blocks)
                            
                            time.sleep(1)
                        

                    for block in peer.finished_blocks:
                        self.piece_manager.update_pieces(block)
                        
                    
                
                
        except KeyboardInterrupt:
            for peer in self.peer_list:
                peer.quit()
            print('keyboard interrupt detected, killing peers')

