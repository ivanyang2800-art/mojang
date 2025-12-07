from tkinter import *
from tkinter import ttk
from tkinter import messagebox as warn
from PIL import ImageTk,Image
from database import Database

class loginpage:
    def __init__(self,root):

        self.root = root
        self.db=Database()

        self.user_id = None
        self.store_id = None        

        self.root.title ("page login")
        self.root.geometry ("500x300")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")


        self.show_base_screen()

    def show_base_screen(self):
        self.base_frame=ttk.Frame(self.root)
        self.base_frame.place(relx=0, rely=0.3,relwidth=1, relheight=1)

        entry_frame=ttk.Frame(self.base_frame)
        entry_frame.pack()

        ttk.Label(entry_frame, text="name").grid(column=0, row=0)
        self.name_entry=ttk.Entry(entry_frame, width=25)
        self.name_entry.grid(column=1,row=0)

        ttk.Label(entry_frame, text="password").grid(column=0,row=1)
        self.password_entry=ttk.Entry(entry_frame, width=25)
        self.password_entry.grid(column=1,row=1)

        button_frame=ttk.Frame(self.base_frame)
        button_frame.pack()

        login_button=ttk.Button(button_frame, text="login", command=self.login_account)
        login_button.grid(column=0,row=0)

        register_button=ttk.Button(button_frame, text="register", command=self.show_register_screen)
        register_button.grid(column=1, row=0)

    def clear_base_frame(self):
        for w in self.base_frame.winfo_children():
            w.destroy()

    def back_base_screen(self):
        for widget in self.root.winfo_children() :
            widget.destroy()
        self.__init__(self.root)

    def show_register_screen(self):
        self.clear_base_frame()


        self.base_frame=ttk.Frame(self.root)
        self.base_frame.place(relx=0, rely=0,relwidth=1, relheight=1)

        back=ttk.Button(self.base_frame,text="back", command=self.back_base_screen)
        back.pack(anchor=NW)

        entry_frame=ttk.Frame(self.base_frame)
        entry_frame.pack(pady=(40,5))

        ttk.Label(entry_frame, text="name").grid(column=0, row=0)
        self.name_entry=ttk.Entry(entry_frame, width=25)
        self.name_entry.grid(column=1,row=0)

        ttk.Label(entry_frame, text="password").grid(column=0,row=1)
        self.password_entry=ttk.Entry(entry_frame, width=25)
        self.password_entry.grid(column=1,row=1)

        button_frame=ttk.Frame(self.base_frame)
        button_frame.pack()

        register_button=ttk.Button(button_frame, text="create", command=self.register_account)
        register_button.grid(column=1, row=0)


    def register_account(self):
        nama=self.name_entry.get().strip()
        password=self.password_entry.get().strip()

        if not nama or not password:
            warn.showerror("Error", "isi woi")
            return
        try:
            self.db.process_data_query(
            "INSERT INTO users (username,password) VALUES (%s,%s)",
                    (nama,password)
            )
            warn.showinfo("Sukses", "gitu dong kalau mau simpan data")
        except Exception as e:
            warn.showerror("Error", f"simpan data aja ngak bisa:\n{e}")

    def login_account(self):
        nama=self.name_entry.get().strip()
        password=self.password_entry.get().strip()

        if not nama or not password:
            warn.showerror("Error", "isi woi")
            return
        try:
            user=self.db.get_data(
            "SELECT id FROM users WHERE username = %s AND password= %s",
                    (nama,password)
            )
            if user:
                self.user_id=user[0]
                self.show_home_frame()
            else:
                warn.showerror("Login Gagal", """sandi atau password salah.\n butut kali ingatan lu""")
        except Exception as e:
            warn.showerror("Error", f"simpan data aja ngak bisa:\n{e}")

    def show_home_frame(self):
        self.clear_window()    

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")

        self.base_frame=ttk.Frame(self.root,border=1)
        self.base_frame.pack(fill=BOTH, expand=TRUE)

        back=ttk.Button(self.base_frame,text="back", command=self.back_base_screen)
        back.pack(anchor=NW)

        menu=ttk.Frame(self.base_frame)
        menu.pack()

        self.search=ttk.Entry(menu, width=25)
        self.search.grid(column=0,row=0)

        self.toko=ttk.Frame(menu)
        self.toko.grid(column=1,row=0)

        self.check_store()

    def check_store(self):
        user=self.db.get_data(
            "SELECT id, store_name FROM stores WHERE user_id = %s",
            (self.user_id,)
        )

        if user:
            self.store_id = user[0]
            btn_store = ttk.Button(
                self.toko,
                text=f"Toko saya: {user[1]}",
                command=self.login_store_user,

            )
            btn_store.pack(pady=10)
        else:
            self.store_id = None
            btn_daftar = ttk.Button(
                self.toko,
                text="Daftar jadi penjual",
                command=self.show_register_store
            )
            btn_daftar.pack(pady=10)
            

    def show_register_store(self):
        self.clear_window()    

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")

        self.base_frame=ttk.Frame(self.root,border=1, relief=SUNKEN)
        self.base_frame.pack(fill=BOTH, expand=TRUE)

        back=ttk.Button(self.base_frame, text="back", command=self.show_home_frame)
        back.pack(anchor=NW)

        title=ttk.Label(self.base_frame, text="bikin toko",font=("Segoe UI",16,"bold") )
        title.pack()

        entry_frame=ttk.Frame(self.base_frame)
        entry_frame.pack()

        ttk.Label(entry_frame, text="nama toko").pack()
        self.entry_name=ttk.Entry(entry_frame, width=25)
        self.entry_name.pack()

        ttk.Label(entry_frame, text="deskirpsi").pack()
        self.entry_desc=ttk.Entry(entry_frame, width=25)
        self.entry_desc.pack()

        button=ttk.Button(self.base_frame, text="enter", command=self.register_store)
        button.pack()

    def register_store(self):
        entry_toko=self.entry_name.get().strip()
        entry_desc=self.entry_desc.get().strip()

        if not entry_toko or not entry_desc:
            warn.showerror("Error", "isi woi")
            return
        try:
            self.db.process_data_query(
                "INSERT INTO stores (user_id,store_name,description) VALUES (%s,%s,%s)",
                (self.user_id,entry_toko,entry_desc)
            )
            warn.showinfo("Sukses", "gitu dong kalau mau simpan data")
        except Exception as e:
            warn.showerror("Error", f"simpan data aja ngak bisa:\n{e}")


    def login_store_user(self):
        self.clear_window()    

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")

        style = ttk.Style()
        style.configure("White.TFrame", background="white")

        self.base_frame=ttk.Frame(self.root)
        self.base_frame.pack(fill=BOTH, expand=TRUE)

        user=self.db.get_data(
            "SELECT store_name FROM stores WHERE id = %s",
            (self.store_id,)
        )
        store_name = user[0] if user else "Toko"


        ttk.Label(self.base_frame,
            text="angap ini nama app",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(20, 10))
        ttk.Label(self.base_frame, text="halaman penjual").pack(pady=(5,25))

        frame_kelola_produk=ttk.Frame(self.base_frame, border=1, relief='raised')
        frame_kelola_produk.pack(fill="x", padx=50)

        ttk.Label(frame_kelola_produk, text="kelola produk", font=("segoe UI", 12, "bold")).pack()
        ttk.Label(frame_kelola_produk,text=f"nama toko{store_name}").pack()

        self.edit_produk=ttk.Button(frame_kelola_produk, text="edit produk")
        self.edit_produk.pack()
        self.add_produk=ttk.Button(frame_kelola_produk, text="tambah produk")
        self.add_produk.pack()
        self.daftar_produk=ttk.Button(frame_kelola_produk, text="lihat daftar")
        self.daftar_produk.pack()
        

        


    
    def clear_window(self) :#buat clear widget saat ini
        for widget in self.root.winfo_children() :
            widget.destroy()
root = Tk()
app=loginpage(root)
root.mainloop()
