from enum import Enum
import Utils

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

class Message:
    def convert_message_id_to_type(self, message_id):
        match message_id:
            case 0:
                return MessageType.CHOKE
            case 1:
                return MessageType.UNCHOKE
            case 2:
                return MessageType.INTERESTED
            case 3:
                return MessageType.NOTINTERESTED
            case 4:
                return MessageType.HAVE
            case 5:
                return MessageType.BITFIELD
            case 6:
                return MessageType.REQUEST
            case 7:
                return MessageType.PIECE
            case 8:
                return MessageType.CANCEL
            case 9:
                return MessageType.PORT
            case _:
                exit(f'Error, unknown message type: {message_id}')

    #builds a message from a socket connection. Blocks until a message has been received
    def from_socket(socket):
        self = Message()
        #get length prefix
        response = socket.recv(4)
        length_prefix = Utils.bytes_to_int(response[0:4])
        
        if not length_prefix:
            self.type = MessageType.KEEPALIVE
            return self
            
        data                = socket.recv(length_prefix)
        message_id          = data[0]
        self.type           = self.convert_message_id_to_type(message_id)
        self.length_prefix  = length_prefix
        
        if self.type == MessageType.HAVE:
            self.payload        =  Utils.bytes_to_int(data[1:])
        elif self.type == MessageType.PIECE:
            self.index        = data[1]#Utils.bytes_to_int(data[1:])
            self.begin        = data[2]#Utils.bytes_to_int(data[1:])
            self.block        = data[3:]#pass
            print(f'processed piece message')
        else:
            self.payload        =  data[1:]
        
        return self
        
    
    #returns the message_type
    def get_type(self):
        return self.type

