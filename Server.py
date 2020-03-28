import socket
from Client import Client
from Connection import Connection
from threading import Thread

HEADERSIZE = 10

class Server():
    connections = []
    peers = []

    socket = {}
    connected = True

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
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket to port and setup to receive connection
        s.bind( ( socket.gethostname(), port ) )
        # listen for incoming connection setups
        s.listen(5)

        Connection.is_server = True
        Server.socket = s

        return s

    def start_server_loop(self, s):
        # the main loop of a peer loops continously, accepting connections
        while Server.connected:
            # this is our local version of the client socket
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established")

            try:
                data = clientsocket.recv(1024)
                if len(data) > 0:
                        print("client message:")
                        print(clientsocket.recv(1024))


                self.server_send_message(clientsocket, "Welcome to the chat")

                # keep a list of the joined users / connections
                Server.connections.append(clientsocket)
                Server.peers.append(address)
            except:
                print("Err: Couldn't reach client!")
                continue
    
    def server_send_message( self, clientsocket, data ):
        # Add fixed length message header describing length buffer should accept
        data = f'{len(data):<{HEADERSIZE}}' + data
            
        clientsocket.send(bytes(data, "utf-8"))
