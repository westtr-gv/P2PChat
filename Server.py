import socket
import threading
from Client import Client


class Server():
    connections = []
    peers = []

    def __init__(self, serverport, userid=None, maxpeers = 5):
        self.serverhost = socket.gethostname()
        self.serverport = int(serverport)
        self.maxpeers = int(maxpeers)

        if userid == None:
            userid = self.serverhost + ":" + str(serverport)
        self.userid = userid


        s = self.initialize_server_socket(self.serverport)

        # the main loop of a peer loops continously, accepting connections
        while True:
            # this is our local version of the client socket
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established")

            try:
                clientsocket.send(bytes("Welcome to the chat", "utf-8"))
                # cThread = threading.Thread(target=self.handle_peer, args= [ conn, self.serverhost ] )
                # cThread.daemon = True
                # cThread.start()

                # keep a list of the joined users / connections
                self.connections.append(clientsocket)
                self.peers.append(address)
            except:
                continue

    
    def initialize_server_socket(self, port):
        # creates a socket that will communicate using the IPv4 (AF_INET) protocol with TCP (SOCK_STREAM).
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        # bind socket to port and setup to receive connection
        s.bind( ( socket.gethostname(), port ) )
        # listen for incoming connection setups
        s.listen(5)

        return s

    
    def sendtopeer( self, peerid, msgtype, msgdata, waitreply=True ):
        if self.router:
            nextpid, host, port = self.router( peerid )
        if not self.router or not nextpid:
            self.__debug( 'Unable to route %s to %s' % (msgtype, peerid) )
            return None
        return self.connectandsend( host, port, msgtype, msgdata, pid=nextpid,
                        waitreply=waitreply )

    
    
    def send_peers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ', '

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))
