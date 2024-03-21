from Tracker import Tracker
from threading import Thread
from Message import Message, MessageType
import Constants
import socket
import ipaddress
import struct
import urllib.parse
import time

'''
This represents a peer in the torrent protocol. After a call to connect(), it will attempt to connect with the remote peer it represents, and it will start
a thread that exchanges messages with the peer and this local torrent client.
Once the peer receives a block, it will store it, so that it can be retrieved by the peermanager, which will in turn add it to the piecemanager.
'''

class Peer:

    def __del__(self):
        try:
            self.socket.close()
        except:
            print('socket was already closed')
 
    def connect(self):
        if self.perform_handshake():
            self.run()
        else:
            self.is_active = False
    
    #file needed to get info hash, which is used for handshake
    def __init__(self, peer_ip, peer_id, peer_port,parsed_metainfo_file):
        self.is_active          = True
        self.new_pieces         = False
        self.available_pieces   = []
        self.finished_blocks    = []
        self.ip                 = ipaddress.ip_address(peer_ip)
        self.id                 = peer_id
        self.port               = peer_port
        self.info_hash          = Tracker.info_to_info_hash_bytes(parsed_metainfo_file[b'info'])
        self.message_queue      = []
        
        #the mandatory state information to keep track of for peers
        self.peer_choking   = True
        self.peer_interested= False
        self.am_choking     = True
        self.am_interested  = False
        self.connect()

    def perform_handshake(self):
        pstrlen         = Constants.PSTRLEN
        pstr            = Constants.PSTR
        reserved_bytes  = bytes([0,0,0,0,0,0,0,0])
        request         = pstrlen + pstr + reserved_bytes + self.info_hash + Constants.PEER_ID.encode('utf-8')
        self.socket     = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if self.ip.version == 4 else socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        
        self.socket.settimeout(Constants.BITTORRENT_TIMEOUT_SECONDS)
        
        try:
            self.socket.connect((str(self.ip), self.port))
            self.socket.sendall(request)
            
            response            = self.socket.recv(68)
            chars_before_hash   = len(pstrlen)+len(pstr)+len(reserved_bytes)
            their_hash          = response[chars_before_hash : chars_before_hash + len(self.info_hash)]
            if not their_hash == self.info_hash:
                self.is_active = False
            print(f'connected to {self.ip}')
            return True
        except Exception as e:
            return False
            
    def send_message(self):#, message):
        if self.is_active:
            if not self.peer_choking and len(self.message_queue) > 0:
                self.socket.sendall(self.message_queue.pop())
            else:
                print('cannot request, peer choking!')
        else:
            print(f'attempted to call socket on inactive client {self.ip}')
    
    
    def send_unchoke_message(self):
        print(f'sending unchoke message to {self.ip}')
        unchoke_message = b'\x00\x00\x00\x01\x01'
        self.message_queue.append(unchoke_message)

    def send_interested_message(self):
        print(f'sending interested message to {self.ip}')
        interested_message = b'\x00\x00\x00\x01\x02'
        self.message_queue.append(interested_message)
    
    
    #should be called from peermanager, piecemanager should be what generates these blocks based on the piece that's available to the peer
    def request_block(self, block):
        message = b'\x00\x00\x00\x0D\x06' + struct.pack(">I",block.index) +struct.pack(">I",block.begin)+ struct.pack(">I", block.length)
        self.message_queue.append(message)

    def queue_block_requests(self, blocks):
        for block in blocks:
            self.request_block(block)
    
    def handle_message(self, msg):
        msg_type = msg.get_type()
        
        if msg_type == MessageType.KEEPALIVE:
            pass
        elif msg_type == MessageType.CHOKE:
            print('peer choking')
            self.peer_choking = True
        elif msg_type == MessageType.UNCHOKE:
            print('peer unchoked')
            self.peer_choking = False
        elif msg_type == MessageType.INTERESTED:
            print('peer interested')
            self.peer_interested = True
        elif msg_type == MessageType.NOT_INTERESTED:
            print('peer not interested')
            self.peer_interested = False
        elif msg_type == MessageType.HAVE:
            print(f'got HAVE, added piece {msg.payload}')
            #appends the index of the advertised piece to the "has pieces" field, useful for peermanager
            self.available_pieces.append(msg.payload)
        elif msg_type == MessageType.BITFIELD:
            print('received bitfield message')
        elif msg_type == MessageType.REQUEST:
            #ignore for now, we don't advertise having any pieces yet
            pass
        elif msg_type == MessageType.PIECE:
            #if it's a piece message, it has an index
            print('WATTAFACK I GOT PIECE ALREADY O.O')
            self.finished_blocks.append(Block.from_message(msg))
            print('Block should be available in finished_blocks now!')
            self.new_pieces = True
        elif msg_type == MessageType.CANCEL:
            #ignore for now, not useful until later
            pass
        elif msg_type == MessageType.PORT:
            #ignore, also not useful for the time being
            pass
    
    
    #an infinite loop, that quits when done or on error. Should add a thread handle to self, so that it can be killed
    def start_exchanging_messages(self):
        while self.is_active:
            msg = Message.from_socket(self.socket)
            self.handle_message(msg)
            self.send_message()
            time.sleep(1)
            
    def has_new_pieces(self):
        return self.new_pieces
        
    #start thread that runs "start_exchanging messages"
    def run(self):
        if self.is_active:
            self.thread_handle = Thread(target=self.start_exchanging_messages)
            self.thread_handle.start()
    
    #signals that we need to stop sending messages, kills the thread
    def quit(self):
        print(f'quitting {self.ip}')
        if self.is_active:
            self.is_active = False
            self.thread_handle.join()

