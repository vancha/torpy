from enum import Enum
from Constants import PEER_ID
import requests
import hashlib
import bencodepy
import urllib.parse

class TrackerResponseType(Enum):
    FAIL = 1,
    WARINING = 2,
    SUCCESS = 3,

class TrackerResponse:
    def from_response(tracker_response):
        pass

class Tracker:

    #a dict that must always have a field called type
    def send_tracker_request(parsed_metainfo_file):
        announce_url    = parsed_metainfo_file[b'announce'].decode('utf-8')

        _info_value     = parsed_metainfo_file[b'info']
        _encoded_value  = bencodepy.encode(_info_value)
        info_hash       = hashlib.sha1(_encoded_value).hexdigest()
        info_hash       = urllib.parse.quote(bytearray.fromhex(info_hash))
        port            = 6881
        try:
            port = parsed_metainfo_file[b'port']
        except:
            pass

        #@todo: temp variables to simplify getting a connection up
        uploaded        = 0
        downloaded      = 0
        left            = parsed_metainfo_file[b'info'][b'length']

        request_url = f"{announce_url}?info_hash={info_hash}&peer_id={PEER_ID}&port={port}&uploaded={uploaded}&downloaded={downloaded}&left={left}&event=started"
        
        try:
            return bencodepy.decode(requests.get(request_url).content)
        except Exception as e:
            exit(f'Failed getting a proper response from the tracker: {e}')

