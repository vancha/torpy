import sys
from Torpy import Torpy
from Constants import PEER_ID

'''
Main entry point to this entire application.
- argument: path to a torrent file
'''
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit('Please call this program with a location to a torrent file as an argument.')
    metainfo_file_location = sys.argv[1]
    torrent_client = Torpy(metainfo_file_location, PEER_ID)
    torrent_client.start_peer_wire_protocol()
