from tkinter import *
from tkinter import ttk
from tkinter import messagebox as warn
from PIL import Image,ImageDraw
import os
import customtkinter
from database import Database



class loginpage:
    def __init__(self,root):

        self.root = root
        self.db=Database()

        self.user_id = None
        self.store_id = None 
        self.cart = []       

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

        title=ttk.Label(menu, text="angap ini nama app atau logo", font=("Segoe UI",16, "bold"))
        title.grid(column=0,row=0, sticky=W)

        self.search=ttk.Entry(menu, width=25)
        self.search.grid(column=1,row=0)

        # optional tombol reset untuk lihat semua lagi
        btn_reset = ttk.Button(menu, text="Reset", command=lambda: self.show_all_products())
        btn_reset.grid(column=3, row=0, padx=5)

        self.toko=ttk.Frame(menu)
        self.toko.grid(column=2,row=0)

        self.check_store()

        # ===== KONTEN BAWAH: Kiri = produk, Kanan = cart =====
        content = ttk.Frame(self.base_frame)
        content.pack(fill=BOTH, expand=True, pady=5)

        # kiri: list produk
        self.products_container = ttk.Frame(content)
        self.products_container.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 5))

        # kanan: cart
        self.cart_frame = ttk.Frame(content, width=220)
        self.cart_frame.pack(side=RIGHT, fill=Y, padx=(5, 10))
        self.cart_frame.pack_propagate(False)

        ttk.Label(self.cart_frame, text="Cart", font=("Segoe UI", 12, "bold")).pack(pady=(5, 5))

        # list item cart
        self.cart_list_frame = ttk.Frame(self.cart_frame)
        self.cart_list_frame.pack(fill=BOTH, expand=True)

        # total + tombol bayar
        self.cart_bottom_frame = ttk.Frame(self.cart_frame)
        self.cart_bottom_frame.pack(fill="x", pady=5)

        self.show_all_products()
        self.refresh_cart()



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

        style = ttk.Style()#kayaknya ini aku gak pakai, malas hapus makanya ada disini
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

        self.add_produk=ttk.Button(frame_kelola_produk, text="tambah produk", command=self.show_add_produk)
        self.add_produk.pack()

        self.daftar_produk=ttk.Button(frame_kelola_produk, text="lihat produk", command=self.show_kelola_product)
        self.daftar_produk.pack()
        back=ttk.Button(frame_kelola_produk,text="back",command=self.show_home_frame)
        back.pack()

    def show_add_produk(self):
        self.clear_window()    

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")

        self.base_frame=ttk.Frame(self.root)
        self.base_frame.pack(fill=BOTH, expand=TRUE, pady=30)

        title=ttk.Label(self.base_frame, text="add product", font=("segoe UI", 12, "bold"))
        title.pack(pady=20)

        frame=ttk.Frame(self.base_frame)
        frame.pack()

        ttk.Label(frame, text="nama barang").grid(column=0,row=0)
        ttk.Label(frame, text="harga").grid(column=0, row=1)
        ttk.Label(frame, text="kuantitas").grid(column=0, row=2)
        ttk.Label(frame, text="deskripsi").grid(column=0, row=3)

        self.insert_name_item=ttk.Entry(frame, width=25)
        self.insert_price_item=ttk.Entry(frame,width=25)
        self.insert_quantity=ttk.Entry(frame,width=25)
        self.insert_desc=ttk.Entry(frame,width=25)

        self.insert_name_item.grid(column=1,row=0)
        self.insert_price_item.grid(column=1,row=1)
        self.insert_quantity.grid(column=1,row=2)
        self.insert_desc.grid(column=1, row=3)

        button_frame=ttk.Frame(self.base_frame)
        button_frame.pack()

        submit=ttk.Button(button_frame, text="submit", command=self.submit_add_item)
        submit.grid(column=1, row=0)

        cancel=ttk.Button(button_frame, text="cancel", command=self.login_store_user)
        cancel.grid(column=0,row=0)

        self.items_container = ttk.Frame(self.root, padding=10)
        self.items_container.pack(fill="both", expand=True)

    def submit_add_item(self):
        self.insert_name=self.insert_name_item.get().strip()
        self.insert_price=self.insert_price_item.get().strip()
        self.insert_quantity=self.insert_quantity.get().strip()
        self.insert_desc=self.insert_desc.get().strip()
        if not self.insert_name or not self.insert_price or not self.insert_quantity:
            warn.showerror("Error", "harus masukan nama, harga, dan quantity")
            return
        try:
            self.item=self.db.process_data_query(
                "INSERT INTO products (store_id,productname,price,quantity,description) VALUES(%s,%s,%s,%s,%s)",
                (self.store_id,self.insert_name,self.insert_price, self.insert_quantity,self.insert_desc)
            )

            warn.showinfo("Sukses", "gitu dong kalau mau simpan data")
        except Exception as e:
            warn.showerror("Error", f"simpan data aja ngak bisa:\n{e}")



    def show_kelola_product(self):
        self.clear_window()    

        self.root.title ("page login")
        self.root.geometry ("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")

        self.base_frame = ttk.Frame(self.root)
        self.base_frame.pack(fill=BOTH, expand=True)

        ttk.Button(self.base_frame, text="back", command=self.login_store_user).pack(anchor=NW)

        ttk.Label(self.base_frame, text="List Produk", font=("Segoe UI", 14, "bold")).pack(pady=10)

        container = ttk.Frame(self.base_frame)
        container.pack(fill="both", expand=True)

        rows = self.db.get_datas(
            "SELECT id, productname, price, quantity FROM products WHERE store_id = %s",
            (self.store_id,)
        )

        for prod_id, name, price, qty in rows:
            item_frame = ttk.Frame(container, border=1, relief="solid", padding=8)
            item_frame.pack(fill="x", pady=5, padx=10)

            ttk.Label(item_frame, text=name, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
            ttk.Label(item_frame, text=f"Rp {price} | Stok: {qty}").grid(row=1, column=0, sticky="w")

            btn_edit = ttk.Button(
            item_frame,
            text="Edit",
            command=lambda pid=prod_id: self.show_edit_item(pid)
        )
            btn_edit.grid(row=0, column=1, rowspan=2, padx=5)

            # (opsional) tombol hapus
            btn_delete = ttk.Button(
                item_frame,
                text="Hapus",
                command=lambda f=item_frame, pid=prod_id: self.delete_item(f, pid)
            )
            btn_delete.grid(row=0, column=2, rowspan=2, padx=5)


    def show_edit_item(self, prod_id):
        self.clear_window()

        self.root.title("Edit Produk")
        self.root.geometry("500x500")
        self.root.iconbitmap(r"c:\Users\Ivan\Downloads\icons\windows_1.ico")

        self.base_frame = ttk.Frame(self.root)
        self.base_frame.pack(fill=BOTH, expand=True, pady=30)

        ttk.Label(self.base_frame, text="Edit Produk", font=("Segoe UI", 12, "bold")).pack(pady=20)

        # ambil data produk dari DB
        row = self.db.get_data(
            "SELECT productname, price, quantity, description FROM products WHERE id = %s",
            (prod_id,)
        )

        if not row:
            warn.showerror("Error", "Produk tidak ditemukan")
            self.show_kelola_product()
            return

        name, price, qty, desc = row

        form = ttk.Frame(self.base_frame)
        form.pack()

        ttk.Label(form, text="Nama Produk").grid(column=0, row=0, sticky="w")
        ttk.Label(form, text="Harga").grid(column=0, row=1, sticky="w")
        ttk.Label(form, text="Kuantitas").grid(column=0, row=2, sticky="w")
        ttk.Label(form, text="Deskripsi").grid(column=0, row=3, sticky="w")

        self.edit_name_entry = ttk.Entry(form, width=25)
        self.edit_price_entry = ttk.Entry(form, width=25)
        self.edit_qty_entry = ttk.Entry(form, width=25)
        self.edit_desc_entry = ttk.Entry(form, width=25)

        self.edit_name_entry.grid(column=1, row=0, pady=2)
        self.edit_price_entry.grid(column=1, row=1, pady=2)
        self.edit_qty_entry.grid(column=1, row=2, pady=2)
        self.edit_desc_entry.grid(column=1, row=3, pady=2)

        # isi value awal
        self.edit_name_entry.insert(0, name)
        self.edit_price_entry.insert(0, price)
        self.edit_qty_entry.insert(0, qty)
        if desc:
            self.edit_desc_entry.insert(0, desc)

        # simpan id produk yang sedang diedit
        self.current_edit_product_id = prod_id

        btn_frame = ttk.Frame(self.base_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Batal", command=self.show_kelola_product).grid(column=0, row=0, padx=5)
        ttk.Button(btn_frame, text="Simpan", command=self.submit_edit_item).grid(column=1, row=0, padx=5)

    def submit_edit_item(self):
        # ambil nilai dari form edit
        name = self.edit_name_entry.get().strip()
        price = self.edit_price_entry.get().strip()
        qty = self.edit_qty_entry.get().strip()
        desc = self.edit_desc_entry.get().strip()

        if not name or not price or not qty:
            warn.showerror("Error", "Nama, harga, dan kuantitas wajib diisi")
            return

        try:
            # update ke database
            self.db.process_data_query(
                "UPDATE products SET productname=%s, price=%s, quantity=%s, description=%s "
                "WHERE id=%s",
                (name, price, qty, desc, self.current_edit_product_id)
            )

            warn.showinfo("Sukses", "Produk berhasil diupdate")

            # balik ke list produk
            self.show_kelola_product()

        except Exception as e:
            warn.showerror("Error", f"Gagal update produk:\n{e}")

    def delete_item(self, frame, prod_id):
        # konfirmasi dulu biar aman
        if not warn.askyesno("Konfirmasi", "Yakin ingin menghapus produk ini?"):
            return

        try:
            # hapus dari database
            self.db.process_data_query(
                "DELETE FROM products WHERE id = %s",
                (prod_id,)
            )

            # hapus tampilan item dari UI
            frame.destroy()

            warn.showinfo("Sukses", "Produk berhasil dihapus")

        except Exception as e:
            warn.showerror("Error", f"Gagal menghapus produk:\n{e}")

    def show_all_products(self, keyword=None):
        # bersihkan tampilan produk lama
        for w in self.products_container.winfo_children():
            w.destroy()

        # query ambil produk + nama toko
        if keyword:
            query = """
                SELECT p.id, p.productname, p.price, p.quantity, s.store_name
                FROM products p
                JOIN stores s ON p.store_id = s.id
                WHERE p.productname LIKE %s
            """
            params = (f"%{keyword}%",)
        else:
            query = """
                SELECT p.id, p.productname, p.price, p.quantity, s.store_name
                FROM products p
                JOIN stores s ON p.store_id = s.id
            """
            params = None

        rows = self.db.get_datas(query, params)

        if not rows:
            ttk.Label(self.products_container, text="Produk tidak ditemukan.", foreground="gray").pack(pady=20)
            return

        for prod_id, name, price, qty, store_name in rows:
            item_frame = ttk.Frame(self.products_container, border=1, relief="solid", padding=8)
            item_frame.pack(fill="x", padx=5, pady=5)

            ttk.Label(item_frame, text=name, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
            ttk.Label(item_frame, text=f"Rp {price} | Stok: {qty}").grid(row=1, column=0, sticky="w")
            ttk.Label(item_frame, text=f"Toko: {store_name}", foreground="gray").grid(row=2, column=0, sticky="w")

            # tombol Add to Cart
            btn_cart = ttk.Button(
                item_frame,
                text="Add to Cart",
                command=lambda pid=prod_id, pname=name, pprice=price, pqty=qty: 
                    self.add_to_cart(pid, pname, pprice, pqty)
            )
            btn_cart.grid(row=0, column=1, rowspan=3, padx=5)


    def refresh_cart(self):
        # bersihin isi list cart
        for w in self.cart_list_frame.winfo_children():
            w.destroy()

        # bersihin total + tombol bayar lama
        for w in self.cart_bottom_frame.winfo_children():
            w.destroy()

        if not self.cart:
            ttk.Label(
                self.cart_list_frame,
                text="Cart kosong",
                foreground="gray"
            ).pack(pady=10)
            return

        total = 0

        for item in self.cart:
            subtotal = item["price"] * item["qty"]
            total += subtotal

            row_frame = ttk.Frame(self.cart_list_frame)
            row_frame.pack(fill="x", pady=2, padx=5)

            ttk.Label(row_frame, text=item["name"]).grid(row=0, column=0, sticky="w")
            ttk.Label(row_frame, text=f"x{item['qty']}").grid(row=0, column=1, padx=3)
            ttk.Label(row_frame, text=f"Rp {int(subtotal)}").grid(row=0, column=2, sticky="e")

            ttk.Button(
                row_frame, text="-", width=2,
                command=lambda pid=item["id"]: self.change_cart_qty(pid, -1)
            ).grid(row=0, column=3, padx=2)

            btn_plus = ttk.Button(
            row_frame,
            text="+",
            width=2,
            command=lambda pid=item["id"]: self.change_cart_qty(pid, +1)
            )
            btn_plus.grid(row=0, column=4, padx=2)

        # bagian total + tombol bayar (SELALU satu kali, karena yang lama sudah dihapus)
        ttk.Label(
            self.cart_bottom_frame,
            text=f"Total: Rp {int(total)}",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=5)

        ttk.Button(
            self.cart_bottom_frame,
            text="Bayar",
            command=self.checkout_cart
        ).pack(fill="x", padx=5, pady=(3, 5))
            
    def add_to_cart(self, product_id, name, price, max_stok):
        # cek apakah produk sudah ada di cart
        for item in self.cart:
            if item["id"] == product_id:

                # cek stok
                if item["qty"] >= max_stok:
                    warn.showwarning("Stok Habis", f"Stok {name} tinggal {max_stok}.")
                    return

                item["qty"] += 1
                break

        else:
            # belum ada, tambahkan item baru
            if max_stok <= 0:
                warn.showwarning("Stok Kosong", "Barang ini tidak tersedia.")
                return

            self.cart.append({
                "id": product_id,
                "name": name,
                "price": float(price),
                "qty": 1,
                "max_stok": max_stok
            })

        self.refresh_cart()

    def change_cart_qty(self, product_id, delta):
        for item in self.cart:
            if item["id"] == product_id:

                # kalau naik tapi sudah max stok → stop
                if delta > 0 and item["qty"] >= item["max_stok"]:
                    warn.showwarning("Melewati Stok!", f"Stok {item['name']} hanya {item['max_stok']}.")
                    return

                item["qty"] += delta

                if item["qty"] <= 0:
                    self.cart.remove(item)
                break

        self.refresh_cart()


    def checkout_cart(self):
        if not self.cart:
            warn.showinfo("Info", "Cart masih kosong.")
            return

        total = sum(item["price"] * item["qty"] for item in self.cart)
        if not warn.askyesno("Konfirmasi", f"Total pembayaran Rp {int(total)}.\nLanjut bayar?"):
            return

        # di sini kamu bisa simpan ke tabel transaksi kalau mau
        # untuk sekarang, anggap berhasil lalu kosongkan cart

        self.cart.clear()
        self.refresh_cart()

        warn.showinfo("Sukses", "Pembayaran berhasil (simulasi).")






    
    def clear_window(self) :#buat clear widget saat ini
        for widget in self.root.winfo_children() :
            widget.destroy()
root = Tk()
app=loginpage(root)
root.mainloop()
