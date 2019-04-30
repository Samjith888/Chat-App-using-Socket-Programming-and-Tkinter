

import getpass
import os
import time
from tkinter import *
from threading import Thread
from tkinter import messagebox
from PIL import ImageTk, Image
import tkinter as tk
import socket
from plyer import notification
from tkinter import filedialog
import os
import ctypes

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
SW_HIDE = 0
hWnd = kernel32.GetConsoleWindow()
user32.ShowWindow(hWnd, SW_HIDE)

root = Tk()
root.title("H-PINGER")
root.geometry("350x200")
root.resizable(width=False, height=False)


from itertools import count

class ImageLabel(tk.Label):

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

def center(toplevel):
    toplevel.update_idletasks()
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2.5 - size[0]/3
    y = screen_height/2.5 - size[1]/3
    toplevel.geometry("+%d+%d" % (x, y))

def handle_client(c, addr):

    def close_after_2s():
        root.iconify()

    root.after(4000, close_after_2s)
    client_username = c.recv(4141)
    client_username = client_username.decode('ascii')

    popup1 = Toplevel()
    popup1.title('Notification')
    popup1.geometry('250x100')
    popup1.attributes('-topmost', 1)
    popup1.attributes('-topmost', 0)
    popup1.resizable(width=False, height=False)
    prompt = " Connected to " + addr[0] + ""
    label1 = Label(popup1, text=prompt, width=len(prompt), font=("Arial", 10))
    label1.place(x=37, y=30, height=39, width=180)
    imgn = ImageTk.PhotoImage(Image.open("user2.png"))
    paneln = Label(popup1, image=imgn)
    paneln.place(x=10, y=30, height=34, width=34)

    def close_after_2s():
        popup1.destroy()

    popup1.after(4000, close_after_2s)

    top = Toplevel()
    top.title('H-PINGER')
    top.geometry("400x500")
    top.attributes('-topmost', 1)
    top.attributes('-topmost', 0)
    center(top)
    top.resizable(width=FALSE, height=FALSE)
    inputentry = Text(top, bd=0, bg="white", width="29", height="5", font=("Arial", 12))
    inputentry.configure(highlightbackground='lightgrey', highlightthickness=1)
    inputentry.bind('<Return>', (lambda event: send()))
    inputentry.place(x=128, y=401, height=90, width=265)
    img = ImageTk.PhotoImage(Image.open("user4.png"))
    panel = Label(top, image=img)
    prompt = client_username
    user_lb = Label(top, text=prompt, width=len(prompt), font=(12,))
    prompt = addr[0]
    ip_lb = Label(top, text=prompt, width=len(prompt), font=("Arial", 8))
    outputtext = Text(top, bd=0, bg="white", height="8", width="50", font=("Arial", 12))
    outputtext.configure(highlightbackground='lightgrey', highlightthickness=1)
    scrollbar = Scrollbar(top, command=outputtext.yview)
    outputtext['yscrollcommand'] = scrollbar.set
    SendButton = Button(top, font=30, text="Send", width="12", height=5, bd=0, command=(lambda: send()))
    send_img = PhotoImage(file="e2.png")  # make sure to add "/" not "\"
    SendButton.config(image=send_img)
    up = Button(top, text="Attach", font=30, width="18", height=3, bd=0, command=(lambda: FileTransfer()))
    upbt_img = PhotoImage(file="at3.png")  # make sure to add "/" not "\"
    up.config(image=upbt_img)

    def disable_event():
        global root
        root.quit()

    def send():

        varContent = inputentry.get("1.0", END)
        varContent = varContent.strip()

        if varContent and (not varContent.isspace()):
            message = varContent.encode("ascii")
            c.send(message)
            message = "\n" + varContent + "\n\n"
            outputtext.tag_config('user_message', justify='right',wrap='word')
            outputtext.insert(tk.END, message, 'user_message')
            outputtext.see(tk.END)
            inputentry.delete('1.0', END)

    def recv():
        while True:
            reply = c.recv(4141)
            reply = reply.decode('ascii')

            chek = 'START_TRANSFER_FILE_NAME#3@41$*='
            if chek in reply:
                # print(reply)
                file_name = reply.split("=", 1)[1]
                scc = socket.socket()
                port = 7676
                host = addr[0]
                scc.connect((host, port))
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
                popup2.resizable(width=False, height=False)
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
                import winsound
                winsound.PlaySound("notif.wav", winsound.SND_ALIAS)

                if 'normal' != top.state():
                    popup3 = Toplevel()
                    popup3.title('Notification')
                    popup3.geometry('250x100')
                    popup3.resizable(width=False, height=False)
                    popup3.attributes('-topmost', 1)
                    popup3.attributes('-topmost', 0)
                    prompt ="Message received from \n" + client_username + ""
                    label3 = Label(popup3, text=prompt, width=len(prompt), font=("Arial", 10))
                    label3.place(x=45, y=32, height=39, width=200)
                    imgn = ImageTk.PhotoImage(Image.open("tick.png"))
                    paneln3 = Label(popup3, image=imgn)
                    paneln3.place(x=14, y=30, height=39, width=30)
                    def close_after_2s():
                        popup3.destroy()

                    popup3.after(6000, close_after_2s)

                    notification.notify(
                        title='New message received',
                        message="Message received from\n " + client_username + "",
                        app_name='H-PINGER',
                        timeout=20,
                        app_icon='3.ico')


    def FileTransfer():
        File_path = filedialog.askopenfilename(title='Choose file to send')
        if File_path:

            File_name = os.path.basename(File_path)
            trnsfr_st = 'START_TRANSFER_FILE_NAME#3@41$*=' + File_name
            message = trnsfr_st.encode("ascii")
            c.send(message)

            port = 6767
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

            ftmessage = "\n" + File_name + "\n\n"
            outputtext.tag_config('u', justify='right', foreground="royalblue")
            outputtext.insert(tk.END, ftmessage, 'u')
            conns.close()

            ss.close()

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
            panel4.place(x=14, y=30, height=39, width=39)

            def close_after_2s():
                popup4.destroy()

            popup4.after(4000, close_after_2s)

    outputtext = Text(top, bd=0, bg="white", height="8", width="50", font=("Arial", 12))
    outputtext.configure(highlightbackground='lightgrey', highlightthickness=1)
    scrollbar = Scrollbar(top, command=outputtext.yview)
    outputtext['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=376, y=40, height=352)
    outputtext.place(x=6, y=40, height=352, width=370)
    inputentry.place(x=6, y=401, height=90, width=265)
    panel.place(x=6, y=1, height=39, width=39)
    SendButton.place(x=285, y=418, height=60, width=62)
    up.place(x=360, y=3, height=32, width=32)
    user_lb.place(x=45, y=4, height=18)
    ip_lb.place(x=50, y=26, height=10)

    while True:
        t2=Thread(target=recv())
        t2.setDaemon(True)
        t2.start()


def onclosing(arg,s):
    # print("trying to close the window")
    if messagebox.askokcancel("Quit", "Do you want to close H-PINGER?"):
        s.close()
        root.destroy()

def accept_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip = '0.0.0.0'
    port = 4141
    s.bind((ip, port))
    s.listen(5)

    time.sleep(1)
    act_lb1.destroy()
    sp.destroy()
    panelu.destroy()
    panelunew.place(x=6, y=6, height=35)
    label1.place(x=20, y=70, height=39, width=180)
    panel.place(x=230, y=67, height=39, width=39)
    # panel.load("checked2.gif")
    labelw.place(x=20, y=120, height=39, width=180)
    panelw.place(x=230, y=120, height=39, width=65)
    panelw.load('124.gif')

    connected_clients = []

    while True:
        root.protocol("WM_DELETE_WINDOW", lambda arg=(root): onclosing(arg, s))
        c, addr = s.accept()

        connected_clients.append(addr[0])
        print(connected_clients)
        user_name=getpass.getuser()
        user_name=user_name.encode("ascii")
        c.send(user_name)

        t = Thread(target=handle_client, args=(c, addr))
        t.setDaemon(True)
        t.start()

def con():

    t = Thread(target=accept_connection)
    t.setDaemon(True)
    t.start()

sp = Button(text='Activate', anchor='center', font=30, width=18, height=3, bd=0, command=con)
act_img = PhotoImage(file='e1.png')
sp.config(image=act_img)
sp.place(x=130, y=100, height=68, width=68)
act_lb1 = Label(text='Press the button to activate')
act_lb1.place(x=100, y=40, height=55)
imgu = ImageTk.PhotoImage(Image.open("user1.png"))
panelu = Label(root, image = imgu)
panelu.place(x=6, y=6, height=35)
slabel1 = Label(text=getpass.getuser())
slabel1.place(x=48, y=8, height=14)
slabel2 = Label(text=socket.gethostbyname(socket.gethostname()))
slabel2.place(x=48, y=30, height=10)
imgunew = ImageTk.PhotoImage(Image.open("user4.png"))
panelunew = Label(root, image=imgunew)
img = ImageTk.PhotoImage(Image.open("checked1.png"))
panel = Label(root, image = img)
prompt1 = "Server Activated"
label1 = Label(root, text=prompt1, width=len(prompt1), font=("Arial",12))
prompt2 = "Waiting new connections"
labelw = Label(root, text=prompt2, width=len(prompt2), font=("Arial",12))
panelw = ImageLabel(root)

root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)
root.mainloop()



