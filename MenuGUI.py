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
        self.filemenu.add_command(label="Connect", command=self.popup)
        self.filemenu.add_command(label="Send Message", command=lambda: ChatGUI.update("send"))
        self.filemenu.add_command(label="Leave Chat", command=lambda: Connection.disconnect())

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command=window.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.editmenu = Menu(self.menubar, tearoff=0)

        self.editmenu.add_command(label="Clear Message", command=ChatGUI.clear_message)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Tutorial", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

    def donothing(self):
        filewin = Toplevel(window)
        button = Button(filewin, text="Do nothing button")
        button.pack()

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
        self.b = Button(top,text='Join Chat',command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()

        c = Connection()
        if not c.is_valid_connection(self.value):
            # make a new popup. warn previous was invalid.
            popupWindow(self.window, "(\"" + self.value + "\" is invalid)")
        else:
            # try connecting to the host
            try:
                client = Client(65432)
            except ConnectionRefusedError:
                 # make a new popup. warn previous was unavailable.
                popupWindow(self.window, "(\"" + self.value + "\" is unavailable)")