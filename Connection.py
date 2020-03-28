import socket, sys, threading

class Connection():
    # class variables
    is_server = False
    is_client = False
    user = ""

    @staticmethod
    def before_close_window(window):
        print("Window closing.")
        Connection.disconnect()
        window.destroy()

    @staticmethod
    def disconnect():
        from Client import Client
        from Server import Server

        if not (Connection.is_client or Connection.is_server):
            print("Nothing to close")
            return

        if Connection.is_server:
            Client.send_message("-- Chat closed --")

            # show it in server's chat since they will be disconnected
            import time
            time.sleep(.01)

        elif Connection.is_client:
            Client.send_message("-- " + Connection.user + " left the chat --")

        if Connection.is_client:
            print("Ending client connection")
            # remove yourself
            if Client.socket in Server.connections:
                Server.connections.remove(Client.socket)
            Client.connected = False
            Client.socket.close()
            Connection.is_client = False
            
        if Connection.is_server:
            print("Ending all client connections")
            for socket in Server.connections:
                if socket in Server.connections:
                    # close
                    socket.close()
                    # remove them from list of connected sockets
                    Server.connections.remove(socket)


            print("Ending server connection")
            Connection.is_server = False
            Server.socket.close()
            Server.connected = False

    def is_valid_connection(self, connection):
        try:
            socket.inet_aton(connection)
            return True
        except socket.error:
            print("\nThis is not a valid IP address.")
            return False