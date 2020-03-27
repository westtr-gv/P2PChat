from tkinter import *
from MenuGUI import MenuGUI
from Client import Client

import emoji

class ChatGUI(Frame):

    def __init__(self, window):
        self.window = window

        self.message = ''


        # Text Widget
        self.message_history = Text(window, wrap=WORD, padx=4, height=28, state=DISABLED, spacing3=4)

        self.label = Label(window, text="Message:")

        self.entry = Text(window, wrap=WORD, padx=4, bg="#d4d4d4")
        self.entry.focus_set()
        # self.entry.bind("<Return>", (lambda event: self.update("send")))

        self.emoji_button = Button(window, text="Emoji", command=lambda: self.update("emoji"))
        self.send_button = Button(window, text="Send", command=lambda: self.update("send"))

        # LAYOUT

        window.columnconfigure(0, weight=1)
        self.message_history.grid(row=0, column=0, sticky=N+E+W)

        self.label.grid(row=1, column=0, sticky=W)
        self.emoji_button.grid(row=1, column=2, sticky=E, pady=4)

        window.grid_rowconfigure(2, weight=1)
        self.entry.grid(row=2, column=0, columnspan=3, sticky=W+E)

        self.send_button.grid(row=3, column=0, columnspan=3, sticky=E, pady=4)

        self.MenuGUI = MenuGUI(window, self)

    def enable_message_history(self):
        self.message_history.config(state='normal')

    def disable_message_history(self):
        self.message_history.config(state='disabled')

    def clear_message(self):
        self.message = ''
        self.entry.delete('1.0', END)

    def add_message(self, message):
        self.enable_message_history()

        # append message to history
        self.message_history.insert(END, self.message + '\n')

        # scroll to bottom of chat
        self.message_history.see(END)

        self.disable_message_history()

    def update(self, method):
        if method == "send":
            self.message = self.entry.get('1.0', END)
            if len(self.message) == 1:
                return


            # prepend the sender and attach to message history
            self.message = "[Me] " + self.message
            self.add_message(self.message)

            # reset message box
            self.clear_message()

        elif method == "emoji":
            print('Opening Emoji Picker')

            # insert the emoji at the current position
            self.entry.insert(self.entry.index(INSERT), " :) ")
        else: # reset
            self.message = ''