from tkinter import *
from tkinter import ttk
from tkinter import messagebox as warn

class loginpage:
    def __init__(self,root):
        self.root = root
        self.root.title ("ECOMMERCE PROLOGUE")
        self.root.geometry ("1980x1600")

        ttk.Label(self.root,text="username :").pack()
        self.entry_username = ttk.Entry(self.root)
        self.entry_username.pack()

        ttk.Label(self.root,text="password :").pack()
        self.entry_password = ttk.Entry(self.root)
        self.entry_password.pack()

        ttk.Button(self.root, text="Login", command = self.proseslogin).pack()
        
    def proseslogin(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        print(f"username is :{username}, password is:{password}")

root = Tk()
app=loginpage(root)
root.mainloop()