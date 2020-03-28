import socket
from threading import Thread
from Connection import Connection

HEADERSIZE = 10

class Client():
    socket = {}
    connected = True

    def __init__(self, clientport, init=True):
        if init:
            self.clienthost = socket.gethostname()
            self.clientport = int(clientport)


            self.s = self.initialize_client_socket(self.clientport)

            self.send_message("Hello server, i am client")

            clientthread = Thread(target = self.start_client_loop, args=[self.s])
            clientthread.setDaemon(True)
            clientthread.start()

    def initialize_client_socket(self, port):
        # creates a socket that will communicate using the IPv4 (AF_INET) protocol with TCP (SOCK_STREAM).
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        
        s.connect((socket.gethostname(), port))

        Connection.is_client = True
        Client.socket = s

        return s

    def start_client_loop(self, s):
        full_msg = ''
        new_msg = True
        while Client.connected:
            try:
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
            except:
                continue

            # decode bytes
            print(full_msg)

    @staticmethod
    def send_message(data):
        from ChatGUI import ChatGUI
        chat = ChatGUI(ChatGUI.window, False)
        chat.add_message(data)

        print("Sending message to server")
        data = f'{len(data):<{HEADERSIZE}}' + data
        Client.socket.send(bytes(data, 'utf-8'))

    def recv_message(self, sock):
        while True:
            data = self.sock.recv(4096)
            if not data:
                break

            # received list of people in chat
            if data[0:1] == b'\x11':
                print('Peers in chat: ')

            print(str(data, 'utf-8'))

