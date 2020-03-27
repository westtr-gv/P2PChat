import socket
from threading import Thread

HEADERSIZE = 10

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
        full_msg = ''
        new_msg = True
        while True:
            # have a stream of data as bytes. we need to decide how big of chunks we want
            msg = s.recv(16)

            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            # decode bytes
            full_msg += msg.decode("utf-8")

            if len(full_msg) - HEADERSIZE == msglen:
                print(full_msg[HEADERSIZE:])

                # now lets show the message on the GUI

                full_msg = ''
                new_msg = True

        # decode bytes
        print(full_msg)

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
