# from tkinter import *
# from tkinter import ttk
# from tkinter import messagebox as warn
# import auth

# auth_obj = auth.Auth()

# class loginpage:
#     def __init__(self,root):
#         self.root = root
#         self.root.title ("ECOMMERCE PROLOGUE")
#         self.root.geometry ("1980x1600")

#         ttk.Label(self.root,text="username :").pack()
#         self.entry_username = ttk.Entry(self.root)
#         self.entry_username.pack()

#         ttk.Label(self.root,text="password :").pack()
#         self.entry_password = ttk.Entry(self.root)
#         self.entry_password.pack()

#         ttk.Button(self.root, text="Login", command = self.proseslogin).pack()

#     def proseslogin(self):
#         username = self.entry_username.get()
#         password = self.entry_password.get()
#         print(f"username is :{username}, password is:{password}")
#         user_db = auth_obj.proses_login(username,password)
#         print(user_db)

# root = Tk()
# app=loginpage(root)
# root.mainloop()



from tkinter import *
from tkinter import ttk
from tkinter import messagebox as warn
from PIL import ImageTk,Image
from database import Database
import auth
import afterlogin

class loginpage:
    def __init__(self,root):#ini window pertama
        # untuk title, dan ukuran
        self.root = root
        self.db=Database()

        self.root.title ("UIB MART")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")
        
        # untuk username sama password di main page
        frame=Frame(root,width=300, height=200, bd=1, relief=RAISED )
        frame.place(relx=0.5, rely=0.4, anchor=CENTER)

        frame_login = ttk.Frame(frame, width=300, height=200)
        frame_login.pack()

        ttk.Label(frame_login,text="name").grid(row=0,column=0,pady=(15,5))
        ttk.Label(frame_login,text="password").grid(row=1,column=0)


        self.entry_name=ttk.Entry(frame_login, width=30)
        self.entry_password=ttk.Entry(frame_login, width=30,show="*")

        self.entry_name.grid(row=0,column=1,padx=15,pady=(15,5))
        self.entry_password.grid(row=1,column=1,padx=10)


        frame_button=ttk.Frame(frame)
        frame_button.pack(padx=10,pady=5)

        btn_simpan = ttk.Button(frame_button, text="Login", command=self.proses_login)
        btn_create =ttk.Button(frame_button, text="create account", command=self.buat_akun)

        btn_simpan.pack(side=LEFT, padx=5,pady=10)
        btn_create.pack(side=LEFT, padx=15,pady=10)

        self.entry_name.bind("<Return>", lambda e:self.entry_password.focus())

        self.entry_password.bind("<Return>", lambda event: self.proses_login())

        # frame table

    def home_tab(self):#ini window utama
        self.clear_window()

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")
# menu_________________________________
        home_menu=Menu(root)
        root.config(menu=home_menu)

        file_menu=Menu(home_menu, tearoff=0)
        home_menu.add_cascade(label="menu", menu=file_menu)
        file_menu.add_command(label="back login", command=self.go_login)
        file_menu.add_separator()
        file_menu.add_command(label="quit", command=root.quit)

        
# # panel______________________________
#         panel_1=PanedWindow(root, relief="raised", bg="red")
#         panel_1.pack(fill=BOTH, expand=1)

#         left_label= ttk.Label(panel_1, text="left label")
#         panel_1.add(left_label)

#         panel_2=PanedWindow (panel_1,orient=VERTICAL, relief="raised")
#         panel_1.add(panel_2)

#         label_1=ttk.Label(panel_2, text="jofhufhsihfieh")
#         label_1.pack()

# _______________________________________________________________

        
        tabel=Frame(root)
        tabel.pack(fill=X)

        style = ttk.Style()
        style.theme_use("clam")  # wajib, agar 'pressed' state bisa muncul

        style.map(
            "Hover.TButton",
            relief=[("pressed", "sunken"), ("active", "sunken")],
            background=[("pressed", "#d0d0d0"), ("active", "#e0e0e0")],
        )

        btn = ttk.Button(tabel, text="Hover me", style="Hover.TButton")
        btn.grid(row=0, column=5, pady=4,padx=10)
        
        btn_ktg=ttk.Button(tabel, text="kategori", width=12,style="Hover.TButton")
        btn_ktg.grid(row=0,column=1, pady=4,padx=10)

        men=ttk.Entry(tabel, width=30)
        men.grid(row=0,column=2, pady=4,padx=10)

        toko=ttk.Button(tabel, text="Buka toko", width=12,style="Hover.TButton", command=self.create_toko)
        toko.grid(row=0,column=3, pady=4,padx=10)

        profil=ttk. Button(tabel, text="profil", command=self.window_profil,style="Hover.TButton")
        profil.grid(row=0, column=4, pady=4,padx=10)
        # ubah state ketika mouse masuk/keluar
        def on_enter(e):
            btn.state(["pressed"])

        def on_leave(e):
            btn.state(["!pressed"])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)        




    def window_profil(self):
        self.clear_window()

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")

        cek=Frame(root, bg="grey" )
        cek.place(relx=0, rely=0.4)

        nama=ttk.Label(cek, text="...")
        nama.pack()

    def create_toko(self):
        
        self.clear_window()

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")

        frame_toko=Frame(root, bg="grey")
        frame_toko.place(relx=0.5, rely=0.4, anchor=CENTER)

        nama=ttk.Label(frame_toko, text="buat toko")
        nama.pack(pady=20)

        cek=Frame(frame_toko, bg="grey" )
        cek.pack()

        lbl_nama=ttk.Label(cek, text="nama toko")
        deskripsi=ttk.Label(cek, text="deskripsi")

        lbl_nama.grid(row=0, column=0,pady=5)
        deskripsi.grid(row=2,column=0)

        nama_toko=ttk.Entry(cek)
        deskrip= ttk.Entry(cek)

        nama_toko.grid(column=0,row=1, pady=(0,20),ipadx=10)
        deskrip.grid(column=0,row=3, pady=(0,20),ipadx=20, ipady=20,padx=10)

        etr=ttk.Button(cek, text="create")
        etr.grid(column=0, row=4)

        label_1=ttk.Button(root,text="back login", command=self.home_tab)
        label_1.place(anchor=NW)        




        
    def buat_akun(self): #ini window buat akun di window pertama
        self.clear_window()

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")


        label_1=ttk.Button(root,text="back login", command=self.go_login)
        label_1.place(anchor=NW)
        
        frame= ttk.Frame(root,width=300, height=200)
        frame.place(relx=0.5, rely=0.4, anchor=CENTER)

        frame_login = ttk.Frame(frame, width=300, height=200)
        frame_login.pack()

        ttk.Label(frame_login,text="name").grid(row=0,column=0,pady=(15,4))
        ttk.Label(frame_login,text="password").grid(row=1,column=0,pady=4)
        ttk.Label(frame_login,text="email").grid(row=2,column=0,pady=4)


        self.entry_name=ttk.Entry(frame_login, width=30)
        self.entry_password=ttk.Entry(frame_login, width=30)
        self.entry_email=ttk.Entry(frame_login, width=30)

        self.entry_name.grid(row=0,column=1, padx=10,pady=(15,4))
        self.entry_password.grid(row=1,column=1,padx=10,pady=4)
        self.entry_email.grid(row=2,column=1,padx=10,pady=4)

        btn_tampil = ttk.Button(frame, text="Create", command=self.insert)
        btn_tampil.pack(pady=10)
        


    def proses_login(self):#ini untuk login ke window utama
        nama = self.entry_name.get().strip()
        password = self.entry_password.get().strip()

        if not nama or not password:
            warn.showwarning("Peringatan", "main tekan aja lu, isi dulu noh  nama sama password")
            return

        
        try:
            if self.db.check_user(nama, password):
                self.home_tab()   # pindah ke window berikutnya
            else:
                warn.showerror("Login Gagal", """sandi atau password salah.\n butut kali ingatan lu""")
        except Exception as e:
            warn.showerror("Error", f"Terjadi kesalahan saat login:\n{e}")



    def insert(self):#buat masukan data ke database di create akun
        nama = self.entry_name.get()
        password=self.entry_password.get()
        email=self.entry_email.get()

        
        if "@" not in email or not email.endswith(".com"):
            warn.showerror("Error", "email apa yang lu masukin? kek gitu kali bah")
            return
        
        elif len(nama)  < 4:
            warn.showerror("error", "masukin yang bener lah, pendek amat nama lu")
            return
        
        try:
            self.db.process_data_query(
                "INSERT INTO customers (name,password,email) VALUES (%s,%s,%s)",
                (nama,password,email)
            )

            
            warn.showinfo("Sukses", "gitu dong kalau mau simpan data")
        except Exception as e:
            warn.showerror("Error", f"simpan data aja ngak bisa:\n{e}")

    def go_login(self):#buat buka window pertama
        self.clear_window()
        self.__init__(self.root)
    
    def clear_window(self) :#buat clear widget saat ini
        for widget in self.root.winfo_children() :
            widget.destroy()


root = Tk()
app=loginpage(root)
root.mainloop()
