import socket
import threading

class Client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address):
        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 65432        # The port used by the server

        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        
        data = s.recv(1024)

        print('Received', repr(data))

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
