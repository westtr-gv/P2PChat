import socket
from Client import Client
from threading import Thread

HEADERSIZE = 10

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

        serverthread = Thread(target = self.start_server_loop, args=[s])
        serverthread.setDaemon(True)
        serverthread.start()

        # make server holder also a client
        c = Client(serverport)
        

    
    def initialize_server_socket(self, port):
        # creates a socket that will communicate using the IPv4 (AF_INET) protocol with TCP (SOCK_STREAM).
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        # bind socket to port and setup to receive connection
        s.bind( ( socket.gethostname(), port ) )
        # listen for incoming connection setups
        s.listen(5)

        return s

    def start_server_loop(self, s):
        # the main loop of a peer loops continously, accepting connections
        while True:
            # this is our local version of the client socket
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established")

            try:
                self.server_send_message(clientsocket, "Welcome to the chat")

                # keep a list of the joined users / connections
                self.connections.append(clientsocket)
                self.peers.append(address)
            except:
                continue
    
    def server_send_message( self, clientsocket, data ):
        # Add fixed length message header describing length buffer should accept
        data = f'{len(data):<{HEADERSIZE}}' + data
            
        clientsocket.send(bytes(data, "utf-8"))
