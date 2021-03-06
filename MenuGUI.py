from tkinter import *
from Connection import Connection
from Server import Server
from Client import Client

class MenuGUI(Frame):

    def __init__(self, window, ChatGUI):
        self.window = window
        self.ChatGUI = ChatGUI

        self.menubar = Menu(window)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Host Chat", command=lambda: Server(65432))
        self.filemenu.add_command(label="Connect", command=lambda: self.popup())
        self.filemenu.add_command(label="Send Message", command=lambda: ChatGUI.update("send"))
        self.filemenu.add_command(label="Leave Chat", command=lambda: Connection.disconnect())

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command=lambda: Connection.before_close_window(self.window))
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.editmenu = Menu(self.menubar, tearoff=0)

        self.editmenu.add_command(label="Clear Conversation", command=ChatGUI.clear_conversation)
        self.editmenu.add_command(label="Clear Message", command=ChatGUI.clear_message)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)


    def popup(self):
        self.w = popupWindow(self.window)
        self.window.wait_window(self.w.top)

    def entryValue(self):
        return self.w.value



class popupWindow(Frame):
    def __init__(self, window, notice = ''):
        self.window = window

        top = self.top = Toplevel(window)
        self.l = Label(top, text="Enter user's IP address: " + notice)
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.l2 = Label(top, text="Enter your name: ")
        self.l2.pack()
        self.e2 = Entry(top)
        self.e2.pack()
        self.b = Button(top,text='Join Chat',command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        self.name = self.e2.get()
        self.top.destroy()

        c = Connection()
        if not c.is_valid_connection(self.value):
            # make a new popup. warn previous was invalid.
            popupWindow(self.window, "(\"" + self.value + "\" is invalid)")
        else:
            # try connecting to the host
            try:
                Connection.user = self.name
                client = Client(65432)
            except ConnectionRefusedError:
                 # make a new popup. warn previous was unavailable.
                popupWindow(self.window, "(\"" + self.value + "\" is unavailable)")