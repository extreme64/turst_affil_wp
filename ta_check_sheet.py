from oauth2client.service_account import ServiceAccountCredentials
import validators
import gspread
import time

import urllib.request
from xml.dom import minidom

# !/usr/bin/python3
from tkinter import *

#  ++ app modules ++
from modules.talinksfromxml import readWpData
from modules.talinksfromgsheet import proccessGoogleDriveData
# +++

from tkinter import scrolledtext
from tkinter import messagebox




# MAIN +++++++ ++++++
top = Tk()

top.title("TA Check")
#setting window size
width = 500
height = 400
screenwidth = top.winfo_screenwidth()
screenheight = top.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
                            (screenheight - height) / 2)
top.geometry(alignstr)
top.resizable(width=False, height=True)

menubar = Menu(top)
file = Menu(menubar, tearoff=0)

def openScript():
    print("hello!")
    messagebox.showinfo('Hello', 'Done!')


def WPReadComm() -> dict:
    wpData =  readWpData()
    str = " ++  WPReadComm() ++ \n\n"
    txt.insert('1.0', str)
    res = proccessGoogleDriveData(wpData)
    if( False != res):
        txt.insert('2.0', res)
        messagebox.showinfo('TA Check', 'Done!')



file.add_command(label="Open", command=openScript)
file.add_command(label="Close")

file.add_separator()

file.add_command(label="Exit", command=top.quit)

menubar.add_cascade(label="File", menu=file)
edit = Menu(menubar, tearoff=0)
edit.add_command(label="Undo")

edit.add_separator()

edit.add_command(label="TA Check")
edit.add_command(label="TA Update", command=WPReadComm)

menubar.add_cascade(label="Run", menu=edit)
help = Menu(menubar, tearoff=0)
help.add_command(label="About")
menubar.add_cascade(label="Info", menu=help)





txt = scrolledtext.ScrolledText(top, width=40, height=10)
txt.grid(column=0, row=0)

top.config(menu=menubar)
top.mainloop()