from enum import Enum

'''
Represents a message in the bittorrent protocol. The messagetype lists all the possible types of messages there are.
'''

class MessageType(Enum):
    KEEPALIVE = 1,
    CHOKE = 2,
    UNCHOKE = 3,
    INTERESTED = 4,
    NOT_INTERESTED = 5,
    HAVE = 6,
    BITFIELD = 7,
    REQUEST = 8,
    PIECE = 9,
    CANCEL = 10,
    PORT = 11

class Message(Enum):
    #builds a message from a socket connection. Blocks until a message has been received
    def from_socket(self, socket):
        #get length prefix
        response = socket.recv(4)#Utils.bytes_to_int(socket.recv(4))
        length_prefix = Utils.bytes_to_int(response[0:4])
        if not length_prefix:
            self.type = MessageType.KEEPALIVE
            return self
        self.payload    = socket.recv(length_prefix)
        self.message_id = payload[0]
        self.length_prefix = length_prefix
        
        return PeerMessage(length_prefix = length_prefix, message_id = message_id, payload=payload[1:])
        
        
    
    #returns the message_type
    def get_type(self):
        return self.type

