from tkinter import *
import socket
from threading import Thread
from Connection import Connection
import re

HEADERSIZE = 10

class Client():
    socket = {}
    connected = True

    def __init__(self, clientport, init=True):
        if init:
            Client.connected = True
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

        try:
            s.connect((socket.gethostname(), port))
        except ConnectionAbortedError as e:
            print("Connection shut down!")
    

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
                    final_msg = full_msg[HEADERSIZE:]

                    # add image if exists
                    # x = re.match(r'(::)([^)]+)(::)', final_msg)
                    x = re.search('::(.*)::', final_msg)
                    if x:
                        # remove from message
                        final_msg = final_msg[0: x.start():] + final_msg[x.end() + 1::]
                    

                    # show it in the chat for all connected users
                    from ChatGUI import ChatGUI
                    chat = ChatGUI(ChatGUI.window, False)
                    # decode the bytes that were sent into utf8
                    chat.add_message(final_msg)


                    # add the image
                    if x:
                        from PIL import Image,ImageTk
                        code = x.group(0)
                        filename = code[2:len(code)-2]
                        img = Image.open(filename)
                        photoImg = ImageTk.PhotoImage(img)

                        ChatGUI.message_history.config(state='normal')
                        ChatGUI.message_history.image_create(INSERT, image = photoImg)
                        # scroll to bottom of chat
                        ChatGUI.message_history.see(END)
                        ChatGUI.message_history.config(state='disabled')
                        # reset
                        x = None


                    full_msg = ''
                    new_msg = True
            except:
                continue

    @staticmethod
    def send_message(data):
        # append a header to notify how many bytes to expect
        data = f'{len(data):<{HEADERSIZE}}' + data
        try:
            # send message to server
            Client.socket.send(bytes(data, 'utf-8'))
            print("Client sent: " + data)
        except BrokenPipeError as e:
            # server disconnected. get out.
            print("Server disconnected. Leaving chat.")
            Client.connected = False
            Client.socket.close()
            Connection.is_client = False

