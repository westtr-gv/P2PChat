import os
from tkinter import *
from MenuGUI import MenuGUI
from Connection import Connection
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk


class ChatGUI(Frame):
    window = {}
    
    message_history = {}
    entry = {}

    def __init__(self, window, init = True):
        if init:
            ChatGUI.window = window

            self.message = ''

            ChatGUI.message_history = Text(window, wrap=WORD, padx=4, height=28, state=DISABLED, spacing3=4)
            ChatGUI.entry = Text(window, wrap=WORD, padx=4, bg="#d4d4d4")


            self.label = Label(window, text="Message:")

            ChatGUI.entry.focus_set()
            # ChatGUI.entry.bind("<Return>", (lambda event: self.update("send")))

            self.emoji_button = Button(window, text="Emoji", command=lambda: self.update("emoji"))
            self.send_button = Button(window, text="Send", command=lambda: self.update("send"))

            # LAYOUT

            window.columnconfigure(0, weight=1)
            ChatGUI.message_history.grid(row=0, column=0, sticky=N+E+W)

            self.label.grid(row=1, column=0, sticky=W)
            self.emoji_button.grid(row=1, column=2, sticky=E, pady=4)

            window.grid_rowconfigure(2, weight=1)
            ChatGUI.entry.grid(row=2, column=0, columnspan=3, sticky=W+E)

            self.send_button.grid(row=3, column=0, columnspan=3, sticky=E, pady=4)

            self.MenuGUI = MenuGUI(window, self)

    def enable_message_history(self):
        ChatGUI.message_history.config(state='normal')

    def disable_message_history(self):
        ChatGUI.message_history.config(state='disabled')

    def clear_message(self):
        self.message = ''
        ChatGUI.entry.delete('1.0', END)

    def clear_conversation(self):
        self.enable_message_history()
        ChatGUI.message_history.delete('1.0', END)
        self.disable_message_history()

    def add_message(self, message):
        self.enable_message_history()

        # append message to history
        ChatGUI.message_history.insert(END, message + '\n')

        # scroll to bottom of chat
        ChatGUI.message_history.see(END)

        self.disable_message_history()

    def update(self, method):
        if method == "send":
            if not Connection.is_client:
                return

            self.message = ChatGUI.entry.get('1.0', END)
            if len(self.message) == 1:
                return

            # insert the image 'code' into the text for later parsing
            if hasattr(ChatGUI.entry, 'photo'):
                sstring_strt = self.message[:ChatGUI.entry.photo.index] 
                sstring_end = self.message[ChatGUI.entry.photo.index:] 
                self.message = sstring_strt + "::" + ChatGUI.entry.photo.path + "::" + sstring_end

            # prepend the sender and attach to message history
            if Connection.user:
                self.message = "[" + Connection.user + "] " + self.message
            else:
                self.message = "[Host] " + self.message


            # Send the message to the Server as the Client
            print("Sending a message to server")
            from Client import Client
            Client.send_message(self.message)

            # reset message box
            self.clear_message()

        elif method == "emoji":
            # show an "Open" dialog box and return the path to the selected file
            # filename = askopenfilename(initialdir=os.getcwd(), title="Select Emoji", filetypes=[("gifs", "*.gif")])
            try:
                filename = "./emojis/smile.gif"

                img = Image.open(filename)
                photoImg = ImageTk.PhotoImage(img)

                pos = ChatGUI.entry.index(INSERT)
                ChatGUI.entry.image_create(pos, image = photoImg)
                ChatGUI.entry.photo = photoImg
                ChatGUI.entry.photo.path = filename
                ChatGUI.entry.photo.index = len(ChatGUI.entry.get('1.0', END))
            except:
                print("Failed to attach emoji")
                return

        else: # reset
            self.message = ''