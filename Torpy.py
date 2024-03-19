from enum import Enum
from Tracker import Tracker, TrackerResponseType
import bencodepy
from PeerManager import PeerManager

'''
The main torrent client. This takes a torrent file, parses it, and creates the PeerManager. 
it takes the following arguments:
- metainfo_file_location (the actual torrent file to parse)
- peer_id, this is the id with which we can represent ourself to the tracker and other peers

after a call to the start_peer_wire_protocol has been made, a PeerManager will be created, and download will begin.
'''

class Torpy:
    #parses the metainfo file, returns the bdecoded results with all values as a dictionary
    def parse_metainfo_file(metainfo_file_location):
        file_handle = open(metainfo_file_location, "rb")
        try:
            return bencodepy.decode(file_handle.read())
        except:
            exit('Could not properly parse the torrent file.') 

    def __init__(self, metainfo_file_location, peer_id):
        self.parsed_metainfo_file   = Torpy.parse_metainfo_file(metainfo_file_location)
        self.tracker_response       = Tracker.send_tracker_request(self.parsed_metainfo_file)
        
    #gets peers from self.tracker_response, opens a thread for each of them with a call to peer.connect
    def start_peer_wire_protocol(self):
        self.peer_manager   = PeerManager(self.tracker_response, self.parsed_metainfo_file)

    

