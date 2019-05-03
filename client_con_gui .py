#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 18:01:26 2019

@author: elzhar
"""

import tkinter as tk
from tkinter import Entry
import tkinter.scrolledtext as st
import socket as sk
import threading as th

s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
s.setsockopt(sk.SOL_SOCKET,sk.SO_REUSEADDR, 1)
host='127.0.0.1'
port=7000


win = tk.Tk()
win.geometry('340x350')
win.title('Client')
chat = st.ScrolledText(win,width = 31,height = 10,font=('Verdana', 16))
chat.grid(row=0,column=0,padx=5,pady=5)
txtbox=Entry(win,width=25)
txtbox.grid(row=1,column=0,padx=10,pady=10)

chat.insert(tk.END,'connecting to server...\n')

s.connect((host,port))

chat.insert(tk.END,'connected successfully\n')


def rec_func(s):
    while True:
        data=s.recv(2048)
        chat.insert(tk.END,data.decode('utf-8'))
        chat.see(tk.END)

rec_thread=th.Thread(target=rec_func,args=(s,))
rec_thread.start()

def send_func():
    msg=txtbox.get()
    chat.insert(tk.END,'Me: '+msg+'\n')
    s.send(msg.encode('utf-8'))
    txtbox.delete(0, 'end')

btn=tk.Button(win,text='send',width=5,height=2,command=send_func)
btn.grid(row=2,column=0,padx=10,pady=10)

win.mainloop()