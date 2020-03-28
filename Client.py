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


            Client.socket = self.initialize_client_socket(self.clientport)

            Client.send_message(self.clienthost + " joined the chat")

            clientthread = Thread(target = self.start_client_loop)
            clientthread.setDaemon(True)
            clientthread.start()

    def initialize_client_socket(self, port):
        # creates a socket that will communicate using the IPv4 (AF_INET) protocol with TCP (SOCK_STREAM).
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        
        s.connect((socket.gethostname(), port))

        Connection.is_client = True
        Client.socket = s

        return s

    def start_client_loop(self):
        full_msg = ''
        new_msg = True
        while Client.connected:
            try:
                # have a stream of data as bytes. we need to decide how big of chunks we want
                msg = Client.socket.recv(16)

                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                # decode bytes
                full_msg += msg.decode("utf-8")

                if len(full_msg) - HEADERSIZE == msglen:
                    print("Client received: ")
                    print(full_msg[HEADERSIZE:])

                    # show it in the chat for all connected users
                    from ChatGUI import ChatGUI
                    chat = ChatGUI(ChatGUI.window, False)
                    # decode the bytes that were sent into utf8
                    chat.add_message(full_msg[HEADERSIZE:])

                    full_msg = ''
                    new_msg = True
            except:
                continue

    @staticmethod
    def send_message(data):
        # append a header to notify how many bytes to expect
        data = f'{len(data):<{HEADERSIZE}}' + data
        # send message to server
        Client.socket.send(bytes(data, 'utf-8'))
        print("Client sent: " + data)

