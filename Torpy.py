from enum import Enum
import time
import Utils
import Peer
import Message
from Tracker import Tracker, TrackerResponseType
import bencodepy
from BlockManager import BlockManager 
from PeerManager import PeerManager

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
            self.peer_manager   = PeerManager(self.tracker_response, self.parsed_metainfo_file[b'info'][b'piece length'])
            while self.peer_manager.has_active_peers():
                self.peer_manager.update()
        except KeyboardInterrupt:
            print('quitting')

    
