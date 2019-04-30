

import getpass
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter.scrolledtext import ScrolledText
from threading import Thread
from tkinter import messagebox
import os.path
import socket
from tkinter import filedialog
import os
from plyer import notification
import winsound
import ctypes
import os

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_HIDE = 0
hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, SW_HIDE)
master = Tk()
master.title("H-PING")
master.geometry('350x200')

def center(toplevel):
    toplevel.update_idletasks()
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2.5 - size[0]/3
    y = screen_height/2.5 - size[1]/3
    toplevel.geometry("+%d+%d" % (x, y))

def handle_server(ip, s):
    master.withdraw()
    server_username = s.recv(4141)
    server_username = server_username.decode('ascii')

    top = Toplevel()
    top.title('H-PING')
    top.geometry("400x500")
    top.attributes('-topmost', 1)
    top.attributes('-topmost', 0)
    center(top)
    top.resizable(width=FALSE, height=FALSE)
    inputentry = Text(top, bd=0, bg="white", width="29", height="5", font=("Arial", 12))
    inputentry.configure(highlightbackground='lightgrey', highlightthickness=1)
    inputentry.bind('<Return>', (lambda event: send()))
    img = ImageTk.PhotoImage(Image.open("user4.png"))
    panel = Label(top, image=img)
    prompt = server_username
    user_lb = Label(top, text=prompt, width=len(prompt), font=(12,))
    prompt = ip
    ip_lb = Label(top, text=prompt, width=len(prompt), font=("Arial", 8))
    SendButton = Button(top, font=30, text="Send", width="12", height=5, bd=0, command=(lambda: send()))
    send_img = PhotoImage(file="e2.png")  # make sure to add "/" not "\"
    SendButton.config(image=send_img)
    up = Button(top, text="Attach", font=30, width="18", height=3, bd=0, command=(lambda: FileTransfer()))
    upbt_img = PhotoImage(file="at3.png")  # make sure to add "/" not "\"
    up.config(image=upbt_img)
    outputtext = Text(top, bd=0, bg="white", height="8", width="50", font=("Arial", 12))
    outputtext.configure(highlightbackground='lightgrey', highlightthickness=1)
    scrollbar = Scrollbar(top, command=outputtext.yview)
    outputtext['yscrollcommand'] = scrollbar.set
    def send():
        varContent = inputentry.get("1.0", END)
        varContent = varContent.strip()
        if varContent and (not varContent.isspace()):
            message = varContent.encode("ascii")
            s.send(message)
            message = "\n" + varContent + "\n\n"
            outputtext.tag_config('user_message', justify='right',wrap='word')
            outputtext.insert(tk.END, message, 'user_message')
            outputtext.see(tk.END)
            inputentry.delete('1.0', END)

    def recv():
        while True:
            reply = s.recv(4141)
            reply = reply.decode('ascii')

            chek = 'START_TRANSFER_FILE_NAME#3@41$*='
            if chek in reply:
                # print(reply)
                file_name = reply.split("=", 1)[1]
                scc = socket.socket()
                port = 6767
                scc.connect((ip, port))
                received_path = os.path.expanduser('~\\Downloads\\')
                with open(received_path + file_name, 'wb') as f:
                    while True:

                        data = scc.recv(1024)

                        f.write(data)

                        if not data:
                            break

                fmessage = "\n" + file_name + "\n\n"
                outputtext.tag_config('r', background="lightsteelblue", foreground="royalblue")
                outputtext.insert(tk.END, fmessage, 'r')
                f.close()
                scc.close()
                popup2 = Toplevel()
                popup2.title('File Received')
                popup2.geometry('250x100')
                popup2.attributes('-topmost', 1)
                popup2.attributes('-topmost', 0)
                prompt = file_name+" received"
                label1 = Label(popup2, text=prompt, width=len(prompt), font=("Arial", 10))
                label1.place(x=45, y=32, height=39, width=200)
                imgn = ImageTk.PhotoImage(Image.open("tick.png"))
                paneln = Label(popup2, image=imgn)
                paneln.place(x=14, y=30, height=39, width=30)
                def close_after_2s():
                    popup2.destroy()
                popup2.after(4000, close_after_2s)

            else:
                reply = "\n" + reply + "\n\n"
                outputtext.tag_config('reply', background="lightsteelblue", foreground="black", wrap='word')
                outputtext.insert(tk.END, reply, 'reply')
                outputtext.see(tk.END)

                winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                winsound.PlaySound("notif.wav", winsound.SND_ALIAS)

                if 'normal' != top.state():
                    popup3 = Toplevel()
                    popup3.title('Notification')
                    popup3.geometry('250x100')
                    popup3.attributes('-topmost', 1)
                    popup3.attributes('-topmost', 0)
                    prompt ="Message received from\n " + server_username + ""
                    label3 = Label(popup3, text=prompt, width=len(prompt), font=("Arial", 10))
                    label3.place(x=45, y=32, height=39, width=200)
                    imgn = ImageTk.PhotoImage(Image.open("tick.png"))
                    paneln3 = Label(popup3, image=imgn)
                    paneln3.place(x=14, y=30, height=39, width=30)
                    def close_after_2s():
                        popup3.destroy()
                    popup3.after(4000, close_after_2s)

                    notification.notify(
                        title='New message received',
                        message="Message received from \n" + server_username + "",
                        app_name='H-PING',
                        timeout=20,
                        app_icon='3.ico')


    def FileTransfer():
            File_path = filedialog.askopenfilename(title='Choose file to send')

            if File_path:
                File_name = os.path.basename(File_path)
                trnsfr_st = 'START_TRANSFER_FILE_NAME#3@41$*=' + File_name
                message = trnsfr_st.encode("ascii")
                s.send(message)
                port = 7676
                ss = socket.socket()
                host = "0.0.0.0"
                ss.bind((host, port))
                ss.listen(5)
                conns, addr = ss.accept()
                while True:
                    b = os.path.getsize(File_path)
                    f = open(File_path, 'rb')
                    l = f.read(b)

                    while (l):
                        conns.send(l)

                        l = f.read(b)
                    f.close()
                    break
                conns.close()
                ss.close()
                # messagebox.showinfo("Success", File_name + " Sent")
                popup4 = Toplevel()
                popup4.title('Success')
                popup4.geometry('250x100')
                popup4.attributes('-topmost', 1)
                popup4.attributes('-topmost', 0)
                prompt = File_name + " Sent"
                label4 = Label(popup4, text=prompt, width=len(prompt), font=("Arial", 10))
                label4.place(x=45, y=32, height=39, width=200)
                img4 = ImageTk.PhotoImage(Image.open("ms1.png"))
                panel4 = Label(popup4, image=img4)
                panel4.place(x=14, y=30, height=39, width=30)
                def close_after_2s():
                    popup4.destroy()

                popup4.after(4000, close_after_2s)

                ftmessage = "\n" + File_name + "\n\n"
                outputtext.tag_config('u', justify='right', foreground="royalblue")
                outputtext.insert(tk.END, ftmessage, 'u')
    scrollbar.place(x=376, y=40, height=352)
    outputtext.place(x=6, y=40, height=352, width=370)
    inputentry.place(x=6, y=401, height=90, width=265)
    panel.place(x=6, y=1, height=39, width=39)
    SendButton.place(x=285, y=418, height=60, width=62)
    up.place(x=360, y=3, height=32, width=32)
    user_lb.place(x=45, y=4, height=18)
    ip_lb.place(x=50, y=26, height=10)
    def onclosing(arg,s):

            s.close()
            top.destroy()
            sys.exit()
    top.protocol("WM_DELETE_WINDOW", lambda arg=(top): onclosing(arg, s))
    while True:
        t2=Thread(target=recv())
        t2.start()

def chat_window(userInput):
  try:

    e1.configure(text=userInput.get())
    ip = userInput.get()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = 4141
    s.connect((ip, port))
    user_name = getpass.getuser()
    user_name = user_name.encode("ascii")
    s.send(user_name)
    t = Thread(target=handle_server, args=(ip, s))
    t.start()

  except Exception as e:
    messagebox.showerror("Error", "Please activate H PINGER in target system first or check IP")
    master.destroy()

def connect(userInput):
        t1 = Thread(target=chat_window(userInput))
        t1.start()
userInput = StringVar()
ll = Label(master, text="IP Address:",  font=("Arial", 10))
ll.config(height=2, width=15)
ll.place(x=15, y=65, height=18)
e1 = Entry(master, textvariable=userInput,width=20, font=("Arial", 12))
e1.bind('<Return>', (lambda event: connect(userInput)))
e1.place(x=120, y=60, height=25)
imgu = ImageTk.PhotoImage(Image.open("user3.png"))
panelu = Label(master, image = imgu)
panelu.place(x=6, y=6, height=35)
slabel1 = Label(text=getpass.getuser(),font=("Arial", 10))
slabel1.place(x=48, y=18, height=14)
ss = Button(text='connect', anchor='center', font=30, width=18, height=3, bd=0, command=(lambda: connect(userInput)))
act_img = PhotoImage(file='e1.png')
ss.config(image=act_img)
ss.place(x=200, y=110, height=68, width=68)

master.mainloop()