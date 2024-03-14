from enum import Enum
import time
import Utils
import Peer
import Message
from Tracker import Tracker, TrackerResponseType
import bencodepy
 


#Torrent client
class Torpy:
    #parses the metainfo file, returns the bdecoded results with all values as a dictionary
    def parse_metainfo_file( metainfo_file_location):
        file_handle = open(metainfo_file_location, "rb")
        try:
            return bencodepy.decode(file_handle.read())
        except:
            exit('Could not properly parse the torrent file.') 

    def __init__(self, metainfo_file_location, peer_id):
        self.parsed_metainfo_file = Torpy.parse_metainfo_file(metainfo_file_location)
        pieces = self.parsed_metainfo_file[b'info'][b'pieces']
        self.tracker_response = Tracker.send_tracker_request(self.parsed_metainfo_file)

    #gets peers from self.tracker_response, opens a thread for each of them with a call to peer.connect
    def start_peer_wire_protocol(self):
        try:
            self.block_manager  = BlockManager() 
            self.peer_manager   = PeerManager(self.tracker_response, self.block_manager)
            while self.peer_manager.has_active_peers() and self.block_manager.not_finished_downloading():
                self.peer_manager.update()#?or any other method that actually keeps track of the peers. Create this peer manager!
        except KeyboardInterrupt:
            print('quitting')

    
