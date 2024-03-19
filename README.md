# Torpy: a CLI torrent client

This is an implementation of the bittorrent protocol, meant to be a learning project.
While some more advanced features are planned, the goal at first is to make it able to actually download something using torents.
___ 


## Reference material
The following link contains a rather detailed description of the inner workings of the torrent protocol. This is what's used as a reference guide while creating this application:

- https://wiki.theory.org/BitTorrentSpecification

___ 


## Project structure
What follows is a quick rundown of all the files in this program, and what they contain.

### main.py: 
the entry point to the program, it requires a torrent file location as an argument
what this does is initialize the Torpy class, and calls "start_peer_wire_protocol" on it, to do just that.

### Torpy.py: 
The main class of the entire torrent app. it requires a location to a torrent file as an argument. Upon
initialization, it decodes said file, and stores the results in itself as self.decoded_metainfo_file.
it has one method called start_peer_wire_protocol, which by way of initiating the peer wire protocol, creates 
an instance of PeerManager.

### PeerManager.py:
Holds the class PeerManager, which is conceptually responsible for keeping a list of peers, and creates an instance of a BlockManager. It should also keep this list of peers populated in case some peers are either not downloading, or for any other reason not active. To do so, it can request new peers from the tracker through the request_more_peers method.
It periodically checks this list of peers, and sees if any of them have received new blocks/pieces. If so, it adds them to the blockmanager.

### PieceManager.py:
The class that's responsible for piecing together all the data that we get from the peers. This one resource should be shared between all Peers, so that peers can know which pieces we already have, and which pieces we still need. Once a peer gets data (which will be blocks: part of a piece), it should be added to the PieceManager so that other peers are made aware of it too.
It's main job is to get individual blocks received by the peers, and turn them back in to pieces. If a full piece is completely downloaded, the piecemanager needs to verify it by checking it's  hash.

### Peer.py:
The class that represents a remote peer. it has a port, an ip, and an id. when it is created, it automatically starts communicating with the remote peer it represents. Starting with an initial handshake, the exchange of messages begins through a call to start_exchanging_messages(). 
which is called as an argument to a thread. All peers receive and send pieces and blocks in their own threads.

___

## How to use
In order to start downloading a file, open your terminal and type:

```
python3 main.py location/to/torrent/file
```