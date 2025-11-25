from tkinter import *
from tkinter import ttk
from tkinter import messagebox as warn
import customtkinter
import auth

auth_obj = auth.Auth()

customtkinter.set_appearance_mode("dark")  # bisa ganti "light" kalau mau terang
customtkinter.set_default_color_theme("blue")  # atau "green" / "dark-blue"

class loginpage:
    def __init__(self,root):
        self.root = root
        self.root.title ("ECOMMERCE PROLOGUE")
        self.root.geometry ("480x620")
        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(True, True)

        #warna bg
        self.canvas = Canvas(root, width=480, height=620, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0, 0, 480, 620, fill="#1a1a2e", outline="")
        self.canvas.create_rectangle(0, 0, 480, 300, fill="#16213e", outline="")

        #logo
        title = customtkinter.CTkLabel(
            root,
            text="ECOMMERCE\nPROLOGUE",
            font=customtkinter.CTkFont(family="Montserrat", size=36, weight="bold"),
            text_color="#00d4ff",   
            width=480
        )
        title.place(x=0, y=80)
        title.configure(anchor="center")

        # Frame tengah putih
        frame = customtkinter.CTkFrame(root,
             corner_radius=20,
             fg_color="#0f3460",
             width=360,
             height=320
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Username
        customtkinter.CTkLabel(
            frame,
            text="Username",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color="#e0e0e0"
        ).place(x=40, y=30)

        self.entry_username = customtkinter.CTkEntry(
            frame,
            placeholder_text="masukkan username",
            width=280,
            height=50,
            corner_radius=12,
            font=customtkinter.CTkFont(size=14)
        )
        self.entry_username.place(x=40, y=65)

        # Password
        customtkinter.CTkLabel(
            frame,
            text="Password",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color="#e0e0e0"
        ).place(x=40, y=130)

        self.entry_password = customtkinter.CTkEntry(
            frame,
            placeholder_text="masukkan password",
            show="•",
            width=280,
            height=50,
            corner_radius=12,
            font=customtkinter.CTkFont(size=14)
        )
        self.entry_password.place(x=40, y=165)

        # Tombol Login
        customtkinter.CTkButton(
            frame,
            text="LOGIN",
            command=self.proseslogin,
            width=280,
            height=50,
            corner_radius=12,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            fg_color="#00d4ff",
            hover_color="#00b0d4",
            text_color="#000000"
        ).place(x=40, y=240)

    def proseslogin(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        print(f"username is :{username}, password is:{password}")
        user_db = auth_obj.proses_login(username,password)
        print(user_db)


root = Tk()
app=loginpage(root)
root.mainloop()