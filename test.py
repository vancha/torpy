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

def info_to_info_hash_bytes(info):
        _encoded_value  = bencodepy.encode(info)
        info_hash       = hashlib.sha1(_encoded_value).hexdigest()
        info_hash       = bytearray.fromhex(info_hash)
        return bytes(info_hash)

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
        request         = PSTRLEN + PSTR + bytes([0,0,0,0,0,0,0,0]) + info_hash + PEER_ID.encode('utf-8')
        socket.sendall(request)

def compare_hash(socket, info_hash):
    try:
        response            = socket.recv(68)
        chars_before_hash   = len(PSTRLEN)+len(PSTR)+len(bytes([0,0,0,0,0,0,0,0]))
        their_hash          = response[chars_before_hash : chars_before_hash + len(info_hash)]
        print(f'{their_hash} <- theirs\n{info_hash}<- ours\n\n')
        return their_hash == info_hash
    except Exception as e:
        return False

#fixed_length no payload
def send_interested_message(sock):
    # Interested message (single byte with value 2)
    interested_message = b'\x00\x00\x00\x01\x02'
    sock.sendall(interested_message)

def send_unchoke_message(sock):
    # Not choking message (single byte with value 1)
    not_choking_message = b'\x00\x00\x00\x01\x01'
    sock.sendall(not_choking_message)


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
                sock.settimeout(60 * 2)
                sock.connect((str(peer[0]), peer[2]))
                send_handshake(sock, info_to_info_hash_bytes(parsed_metainfo_file[b'info']))
                if not compare_hash(sock, info_to_info_hash_bytes(parsed_metainfo_file[b'info'])):
                    continue
                #here we are connected to the peer, we can start the peer wire protocol (when we are unchoked by the peer)
                peer_choking    = True
                am_interested   = False
                am_choking      = True
                
                while True:
                    while peer_choking:
                        length_prefix = sock.recv(4)
                        if not length_prefix:
                            continue #this was likely a keepalive message
                        length_prefix = int.from_bytes(length_prefix, byteorder='big')
                        print(f'received prefix of {length_prefix}')
                        message_payload = sock.recv(length_prefix)
                        message_id  = message_payload[0]
                        #unchoke
                        message_id
                        if message_id == b'\x01':
                            print('unchoke received!')
                            peer_choking = False
                            continue
                    
                    print('sending interested message')
                    send_interested_message()
                    print('sending unchoke message to peer')
                    send_unchoke_message()
                    
                    
                    length_prefix = sock.recv(4)
                    if not length_prefix:
                        continue #this was likely a keepalive message
                        
                    length_prefix   = int.from_bytes(length_prefix, byteorder='big')
                    message_payload = sock.recv(length_prefix)
                    message_id      = message_payload[0]
                    
                    #choke
                    if message_id == b'\x00':
                        peer_choking = True
                        continue
                    #unchoke
                    if message_id == b'\x01':
                        #if peer was choking we would have gotten stuck in the previous while loop
                        pass
                    #interested
                    if message_id == b'\x02':
                        print('got interested message')
                    #not interested
                    if message_id == b'\x03':
                        print('got not interested message')
                    #have
                    if message_id == b'\x04':
                        print('got have message')
                    #bitfield
                    if message_id == b'\x05':
                        print('got bitfield message')
                    #request
                    if message_id == b'\x06':
                        print('got request message')
                    #piece
                    if message_id == b'\x07':
                        print('got piece message')
                        
                    
                
        except Exception as e:
            print(f'could not connect to {peer[0]} because {e}')
  
  
