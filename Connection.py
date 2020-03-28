import socket, sys, threading

class Connection():
    # class variables
    is_server = False
    is_client = False
    user = ""

    @staticmethod
    def disconnect():
        from Client import Client
        from Server import Server

        if not (Connection.is_client or Connection.is_server):
            print("Nothing to close")
            return

        if Connection.is_client:
            print("Ending client connection")
            # remove yourself
            print("REMOVING SELF FIRST")
            print(Server.connections)
            print(Client.connections)
            Server.connections.remove(Client.socket)
            Client.connected = False
            Client.socket.close()
            Connection.is_client = False
            
        if Connection.is_server:
            print("Ending all client connections")
            Server.connected = False
            for index, socket in Server.connections:
                # close
                socket.close()
                # remove them from list of connected sockets
                del Server.connections[index]

            print("Ending server connection")
            Server.socket.close()
            Connection.is_server = False

    def is_valid_connection(self, connection):
        try:
            socket.inet_aton(connection)
            return True
        except socket.error:
            print("\nThis is not a valid IP address.")
            return False