import customtkinter as ctk
from tkinter import PhotoImage
from database import Database
from CTkMessagebox import CTkMessagebox
from PIL import Image
from afterlogin import HomePage
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.title("UIB MART - Login")
        self.geometry("950x600")
        self.minsize(900, 550)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.grid(row=0, column=0, sticky="nsew")

        self.show_login_page()

    # Placeholder function
    def set_placeholder(self, widget, text, is_password=False):
        widget.insert(0, text)
        widget.configure(text_color="gray")
        if is_password:
            widget.configure(show="")
        def on_focus_in(event):
            if widget.get() == text:
                widget.delete(0, "end")
                widget.configure(text_color="black")
                if is_password:
                    widget.configure(show="*")
        def on_focus_out(event):
            if widget.get() == "":
                widget.insert(0, text)
                widget.configure(text_color="gray")
                if is_password:
                    widget.configure(show  ="")
        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)

    # LOGIN PAGE
    def show_login_page(self):
        for widget in self.container.winfo_children():
            widget.destroy()
    
        self.title("UIB MART - LOGIN")
        # TOP BAR
        top = ctk.CTkFrame(self.container, fg_color="white")
        top.pack(fill="x", pady=10, padx=20)

        try:
            icon = ctk.CTkImage( light_image=Image.open("C:/Users/Lenovo/OneDrive/Documents/GitHub/mojang/img/Logo-UIB.jpg"),
                                size=(50, 50))
       
        except:
            icon = None

        if icon:
            icon_label = ctk.CTkLabel(top, image=icon, text="")
            icon_label.image = icon
            icon_label.pack(side="left")

        title = ctk.CTkLabel(top, text="UIB MART", font=("Arial Rounded MT Bold", 28), text_color="#003773")
        title.pack(side="left", padx=10)


        # MAIN LOGIN CONTAINER
        frame = ctk.CTkFrame(self.container, corner_radius=25, fg_color="#f0f0f5")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        welcome = ctk.CTkLabel(frame, text="Welcome Back to UIB MART", font=("Arial Rounded MT Bold", 26))
        welcome.pack(pady=(10, 5))

        lbl = ctk.CTkLabel(frame, text="LOGIN", font=("Arial Rounded MT Bold", 23))
        lbl.pack(pady=8)

        self.username_entry = ctk.CTkEntry(frame, width=280, height=45, corner_radius=15)
        self.username_entry.pack(pady=10)
        self.set_placeholder(self.username_entry, "Username")

        self.password_entry = ctk.CTkEntry(frame, width=280, height=45, show="*", corner_radius=15)
        self.password_entry.pack(pady=10)
        self.set_placeholder(self.password_entry, "Password", is_password=True)

        login_btn = ctk.CTkButton(
            frame,
            text="Login",
            width=200,
            height=45,
            corner_radius=20,
            hover_color="#1d4ed8",
            fg_color="#003773",
            command=self.login_user
        )
        login_btn.pack(pady=7)

        switch_btn = ctk.CTkButton(
            frame,
            text="Create Account",
            width=200,
            height=45,
            corner_radius=20,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.show_signup_page
        )
        switch_btn.pack(pady=7)

        
        exit_btn = ctk.CTkButton(
            frame,
            text="Exit",
            width=200,
            height=45,
            corner_radius=20,
            fg_color="#ba2f2f",
            hover_color="#811717",
            command=self.destroy
            )
        exit_btn.pack(pady=7)

    # SIGN UP PAGE
    def show_signup_page(self):
        
        for widget in self.container.winfo_children():
            widget.destroy()

        self.title("UIB MART - SIGN UP")
        top = ctk.CTkFrame(self.container, fg_color="white")
        top.pack(fill="x", pady=10, padx=20)

        try:
            icon = ctk.CTkImage( light_image=Image.open("C:/Users/Lenovo/OneDrive/Documents/GitHub/mojang/img/Logo-UIB.jpg"),
                                size=(50, 50))
       
        except:
            icon = None

        if icon:
            icon_label = ctk.CTkLabel(top, image=icon, text="")
            icon_label.image = icon
            icon_label.pack(side="left")

        title = ctk.CTkLabel(top, text="UIB MART", font=("Arial Rounded MT Bold", 28), text_color="#003773")
        title.pack(side="left", padx=10)

        frame = ctk.CTkFrame(self.container, corner_radius=25, fg_color="#f0f0f5")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        welcome = ctk.CTkLabel(frame, text="Welcome to UIB MART", font=("Arial Rounded MT Bold", 26))
        welcome.pack(pady=(10, 5))

        lbl = ctk.CTkLabel(frame, text="CREATE ACCOUNT", font=("Arial Rounded MT Bold", 23))
        lbl.pack(pady=8)

        self.new_username = ctk.CTkEntry(frame, width=280, height=45, corner_radius=15)
        self.new_username.pack(pady=10)
        self.set_placeholder(self.new_username, "Choose Username")

        self.new_password = ctk.CTkEntry(frame, width=280, height=45, corner_radius=15, show="*")
        self.new_password.pack(pady=10)
        self.set_placeholder(self.new_password, "Choose Password", is_password=True)

        signup_btn = ctk.CTkButton(
            frame,
            text="Sign Up",
            width=200,
            height=45,
            corner_radius=20,
            fg_color="#003773",
            hover_color="#1d4ed8",
            command=self.signup_user
        )
        signup_btn.pack(pady=15)

        back_btn = ctk.CTkButton(
            frame,
            text="Back to Login",
            width=200,
            height=45,
            corner_radius=20,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.show_login_page
        )
        back_btn.pack(pady=5)

                
        exit_btn = ctk.CTkButton(
            frame,
            text="Exit",
            width=200,
            height=45,
            corner_radius=20,
            fg_color="#ba2f2f",
            hover_color="#811717",
            command=self.destroy
            )
        exit_btn.pack(pady=7)

    # LOGIN LOGIC
    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in ["", "Username"] or password in ["", "Password"]:
            CTkMessagebox(title="Error", message="Isi username dan password dulu ya!", icon="warning")
            return
        
        if len(username) < 4 or len(password) < 4:
            CTkMessagebox(title="Error", message="Minimal 4 karakter!", icon="warning")
            return

        user = self.db.check_user(username, password)

        if user:
            CTkMessagebox(title="Success", message=f"Selamat datang, {user[1]}!", icon="check", fade_in_duration=300)
            
            # TUTUP LOGIN, BUKA HOME
            self.destroy()                          # tutup jendela login
            home_root = ctk.CTk()                   # bikin jendela baru
            HomePage(home_root, username=user[1])   # buka halaman afterlogin + kirim nama
            home_root.mainloop()
        else:
            CTkMessagebox(title="Error", message="Username atau password salah!", icon="cancel")

    # SIGNUP LOGIC
    def signup_user(self):
        username = self.new_username.get()
        password = self.new_password.get()

        if username == "" or password=="" or password=="Choose Password":
            CTkMessagebox(title="Error", message="Please fill in your username and password correctly!", icon="warning")
            return
        if len(username) < 4:
            CTkMessagebox(title="Error", message="Please pick a longer username (min 4 characters)", icon="warning")
            return
        if len(password) < 6:
            CTkMessagebox(title="Error", message="Please enter a longer password (min 6 characters)", icon="warning")
            return   


        
        self.db.create_user(username, password)
        CTkMessagebox(title="Success", message="Account created successfully!", icon="check")
        self.show_login_page()


# Run app
if __name__ == "__main__":
    app = App()
    app.mainloop()
