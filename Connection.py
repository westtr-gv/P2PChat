import socket, sys, threading
from Client import Client
from Server import Server

class Connection():

    def is_valid_connection(self, connection):
        try:
            socket.inet_aton(connection)
            return True
        except socket.error:
            print("\nThis is not a valid IP address.")
            return False