from tkinter import *
from ChatGUI import ChatGUI
from Server import Server

window = Tk()

def main():
    window.title("P2PChat")
    window.geometry("300x600")

    _chat_gui = ChatGUI(window)
    
    window.config(menu=_chat_gui.MenuGUI.menubar)
    window.minsize(300,600)
    # window.maxsize(400,600)
    window.configure(background='#fff')

    window.protocol("WM_DELETE_WINDOW", before_close_window)
    window.mainloop()

def before_close_window():
    print("Window closing.")
    window.destroy()
  
if __name__== "__main__":
    main()