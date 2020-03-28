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


        Server.socket = self.initialize_server_socket(self.serverport)

        serverthread = Thread(target = self.start_server_loop)
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

        return s

    def start_server_loop(self):
        # the main loop of a peer loops continously, accepting connections
        while Server.connected:
            # this is our local version of the client socket
            clientsocket, address = Server.socket.accept()
            print(f"Connection from {address} has been established")

            handlerthread = Thread(target = self.handler,args=(clientsocket,))
            handlerthread.setDaemon(True)
            handlerthread.start()

            # keep a list of the joined users / connections
            Server.connections.append(clientsocket)
            Server.peers.append(address)

    def handler(self, client):
        full_msg = ''
        new_msg = True

        while Server.connected:
            try:
                # have a stream of data as bytes. we need to decide how big of chunks we want
                msg = client.recv(16)

                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                # decode bytes
                full_msg += msg.decode("utf-8")

                if len(full_msg) - HEADERSIZE == msglen:
                    print("Server received: ")
                    print(full_msg[HEADERSIZE:])

                    # got message. distribute to all recipients
                    for participant in Server.connections:
                        Server.send_message(participant, full_msg[HEADERSIZE:])

                    # reset
                    full_msg = ''
                    new_msg = True
            except:
                continue

    @staticmethod
    def send_message(client, data):
        # append a header to notify how many bytes to expect
        data = f'{len(data):<{HEADERSIZE}}' + data
        # send message to server
        client.send(bytes(data, 'utf-8'))
        print("Client sent: " + data)