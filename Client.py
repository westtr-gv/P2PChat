import socket
from threading import Thread

class Client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, clientport):
        self.clienthost = socket.gethostname()
        self.clientport = int(clientport)


        s = self.initialize_client_socket(self.clientport)

        clientthread = Thread(target = self.start_client_loop, args=[s])
        clientthread.setDaemon(True)
        clientthread.start()

    def initialize_client_socket(self, port):
        # creates a socket that will communicate using the IPv4 (AF_INET) protocol with TCP (SOCK_STREAM).
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        
        s.connect((socket.gethostname(), port))

        return s

    def start_client_loop(self, s):
        while True:
            # have a stream of data as bytes. we need to decide how big of chunks we want
            msg = s.recv(4096)

            # decode bytes
            print(msg.decode("utf-8"))

    def send_message(self, message):
        print("Sending message to server")
        self.sock.send(bytes(message, 'utf-8'))

    def recv_message(self, sock):
        while True:
            data = self.sock.recv(4096)
            if not data:
                break

            # received list of people in chat
            if data[0:1] == b'\x11':
                print('Peers in chat: ')

            print(str(data, 'utf-8'))
