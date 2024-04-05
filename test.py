import sys
import hashlib
import urllib
import requests
import bencodepy
import ipaddress
import socket

PEER_ID = "thurmanmermanddddddd"
PSTRLEN             = b'\x13'
PSTR                = b'BitTorrent protocol'
NUMBER_OF_CHARS_BEFORE_HASH = len(PSTRLEN)+len(PSTR)+len(bytes([0,0,0,0,0,0,0,0]))

'''
Main entry point to this entire application.
- argument: path to a torrent file
'''
def info_to_urlencoded_info_hash(info):
        _encoded_value  = bencodepy.encode(info)
        info_hash       = hashlib.sha1(_encoded_value).hexdigest()
        info_hash       = urllib.parse.quote(info_hash)
        info_hash       = urllib.parse.quote(bytearray.fromhex(info_hash))
        return info_hash
        
def parse_metainfo_file(metainfo_file_location):
        file_handle = open(metainfo_file_location, "rb")
        try:
            return bencodepy.decode(file_handle.read())
        except:
            exit('Could not properly parse the torrent file.')

def send_tracker_request(parsed_metainfo_file):
        announce_url    = parsed_metainfo_file[b'announce'].decode('utf-8')
        info_hash       = info_to_urlencoded_info_hash(parsed_metainfo_file[b'info'])
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

def send_handshake(socket, info_hash):
        request         = PSTRLEN + PSTR + bytes([0,0,0,0,0,0,0,0]) + info_hash + Constants.PEER_ID.encode('utf-8')
        socket.sendall(request)

def compare_hash(socket, info_hash):
    try:
        response            = socket.recv(68)
        chars_before_hash   = len(PSTRLEN)+len(PSTR)+len(bytes([0,0,0,0,0,0,0,0]))
        their_hash          = response[chars_before_hash : chars_before_hash + len(info_hash)]
        
        return their_hash == info_hash
    except Exception as e:
        return False
            
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit('Please call this program with a location to a torrent file as an argument.')
    #get torrent file
    metainfo_file_location  = sys.argv[1]
    #bdecode it
    parsed_metainfo_file    = parse_metainfo_file(metainfo_file_location)
    #request peers from tracker
    tracker_response       =  send_tracker_request(parsed_metainfo_file)
    
    #try to connect with peers from list
    for peer in [(ipaddress.ip_address(peer[b'ip'].decode('utf-8')), peer[b'peer id'], peer[b'port'])  for peer in tracker_response[b'peers']]:
        try:
            #create the socket, set the timeout, and connect to the socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) if peer[0].version == 4 else socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                print('set timeout')
                sock.connect((str(peer[0]), peer[2]))
                print('connected')
                send_handshake(sock)
                if not compare_hash(sock, info_to_urlencoded_info_hash(parsed_metainfo_file[b'info'])):
                    continue
                
        except Exception as e:
            print(f'could not connect to {peer[0]} because {e}')
  
  
