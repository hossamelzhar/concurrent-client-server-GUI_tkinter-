#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 03:12:31 2019

@author: elzhar
"""
import tkinter as tk
from tkinter import Entry
import tkinter.scrolledtext as st
import socket as sk
import threading as th

win = tk.Tk()
win.geometry('340x350')
win.title('Server')
chat = st.ScrolledText(win,width = 31,height = 10,font=('Verdana', 16))
chat.grid(row=0,column=0,padx=5,pady=5)
chat.insert(tk.END,'start chat with clients...\n')
txtbox=Entry(win,width=25)
txtbox.grid(row=1,column=0,padx=10,pady=10)


s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
s.setsockopt(sk.SOL_SOCKET,sk.SO_REUSEADDR, 1)
host='127.0.0.1'
port=7000
clients=[]
s.bind((host,port))
s.listen(7)

chat.insert(tk.END,'waiting for clients...\n')


def send_func():
    global c
    msg=txtbox.get()
    msg='Server: '+msg+'\n'
    chat.insert(tk.END,msg)
    txtbox.delete(0, 'end')
    c.send(msg.encode('utf-8'))

btn=tk.Button(win,text='send',width=5,height=2,command=send_func)
btn.grid(row=2,column=0,padx=10,pady=10)

def recv_func(c,ad):
    while True:
        x=c.recv(2048)
        y=ad+': '+x.decode('utf-8')+'\n'
        chat.insert(tk.END,y)
        chat.see(tk.END)
            
def accpt_client():    
            while True:
                c,ad=s.accept()
                chat.insert(tk.END,'New connection from '+ad[0]+'\n')
                clients.append(c)
                rcv_thrd=th.Thread(target=recv_func,args=(c,ad[0]))
                rcv_thrd.start()
    
accpt_th=th.Thread(target=accpt_client)
accpt_th.start()


win.mainloop()