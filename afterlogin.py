import customtkinter as ctk
from PIL import Image, ImageDraw
import os
from CTkMessagebox import CTkMessagebox
from database import Database
from datetime import datetime

# Theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def buat_placeholder(size=(180, 180)):
    img = Image.new("RGB", size, "#f0f0f0")
    draw = ImageDraw.Draw(img)
    for i in range(-size[0], size[1] * 2, 40):
        draw.line([(i, 0), (i + size[1], size[1])], fill="#e0e0e0", width=20)
        draw.line([(0, i), (size[0], i + size[0])], fill="#e0e0e0", width=20)
    # simple text center (no custom font to avoid dependency)
    tx = "No Image"
    text_x = size[0] // 2 - (len(tx) * 4)
    text_y = size[1] // 2 - 10
    draw.text((text_x, text_y), tx, fill="#aaaaaa")
    return img


class HomePage(ctk.CTk):
    def __init__(self, username="User"):
        super().__init__()
        self.username = username

        # database helper
        self.db = Database()
        # try to get userid & role
        try:
            self.db.cursor.execute("SELECT userid, roleuser FROM userdata WHERE username=%s", (self.username,))
            row = self.db.cursor.fetchone()
            if row:
                self.userid = row[0]
                self.role = row[1]
            else:
                self.userid = None
                self.role = "customer"
        except Exception as e:
            print("DB error while fetching user:", e)
            self.userid = None
            self.role = "customer"

        self.title("UIB MART - Home")
        self.geometry("1200x800")

        ctk.CTkLabel(self, text=f"Selamat datang, {self.username}!",
                     font=("Arial Rounded MT Bold", 28), text_color="#003773").pack(pady=10)

        # HEADER (Judul + lokasi)
        header = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#ffffff")
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="UIB MART",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="#003773"
        ).place(x=20, y=30)

        ctk.CTkLabel(
            header,
            text="INSTAN BATAM",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        ).place(x=20, y=60)

        # === SCROLLABLE PRODUCT GRID ===
        self.container = ctk.CTkScrollableFrame(self, fg_color="#f9f9f9")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # columns
        for i in range(5):
            self.container.grid_columnconfigure(i, weight=1)

        # load products from DB, fallback to sample
        self.products = self.load_products()

        for idx, prod in enumerate(self.products):
            self.create_product_card(self.container, idx, prod)

        # === BOTTOM NAVIGATION (Cart - Home - Akun) ===
        bottom_nav = ctk.CTkFrame(self, height=80, fg_color="white", corner_radius=0)
        bottom_nav.pack(fill="x", side="bottom")
        bottom_nav.pack_propagate(False)

        # Cart (replacing Inbox)
        btn_cart = ctk.CTkButton(
            bottom_nav, text="Cart", width=80, fg_color="transparent",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#999999",
            hover_color="#f0f0f0", command=self.open_cart
        )
        btn_cart.place(x=60, y=25)

        # keluar center button
        btn_keluar = ctk.CTkButton(
            bottom_nav, text="Keluar", width=100, height=50,
            fg_color="#003773", text_color="white", corner_radius=25,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.logout
        )
        btn_keluar.place(relx=0.5, rely=0.5, anchor="center")

        # Akun (ikon orang) with menu
        btn_profile = ctk.CTkButton(
            bottom_nav, text="Akun", width=80, fg_color="transparent",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#003773",
            hover_color="#f0f0f0", command=self.open_account_menu
        )
        btn_profile.place(x=340, y=25)

    # --------------------------- DATABASE HELPERS ---------------------------
    def load_products(self):
        products = []
        try:
            # no description column used anymore
            self.db.cursor.execute("SELECT productid, productname, price, quantity FROM products")
            rows = self.db.cursor.fetchall()
            for r in rows:
                products.append({
                    "productid": r[0],
                    "name": r[1],
                    "price": float(r[2]) if r[2] is not None else 0,
                    "stock": int(r[3]) if r[3] is not None else 0,
                })
        except Exception as e:
            print("Failed to load products from DB, using fallback sample. Error:", e)
            # fallback sample with updated quantities
            products = [
                {"productid": 1, "name": "Sofa", "price": 100000, "stock": 100},
                {"productid": 2, "name": "Lampu", "price": 25000, "stock": 100},
                {"productid": 3, "name": "Meja", "price": 75000, "stock": 100},
            ]
        return products

    def get_or_create_cart(self):
        if not self.userid:
            return None
        try:
            self.db.cursor.execute("SELECT cartid FROM cart WHERE userid=%s AND checkout IS NULL", (self.userid,))
            row = self.db.cursor.fetchone()
            if row:
                return row[0]
            # create
            now = None
            self.db.cursor.execute("INSERT INTO cart (userid, checkout) VALUES (%s, %s)", (self.userid, now))
            self.db.db.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print("get_or_create_cart error:", e)
            return None

    # --------------------------- UI: PRODUCT CARDS ---------------------------
    def create_product_card(self, parent, idx, prod):
        row = idx // 5
        col = idx % 5

        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color="white",
            border_width=1,
            border_color="#eeeeee",
            width=220
        )
        card.grid(row=row, column=col, padx=10, pady=12, sticky="nsew")
        card.bind("<Button-1>", lambda e, p=prod: self.show_detail(p))

        # Gambar (placeholder)
        img = buat_placeholder()
        ctk_img = ctk.CTkImage(light_image=img, size=(180, 180))
        lbl_img = ctk.CTkLabel(card, image=ctk_img, text="")
        lbl_img.image = ctk_img
        lbl_img.pack(pady=8)

        # Nama produk
        ctk.CTkLabel(card, text=prod["name"], font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#222222", wraplength=170, justify="center").pack(pady=5)

        # Stock di bawah nama dan di atas harga
        stock_text = f"Stock: {prod['stock']}" if prod.get('stock') is not None else "Stock: -"
        ctk.CTkLabel(card, text=stock_text, font=ctk.CTkFont(size=12), text_color="#666666").pack(pady=(0, 5))

        # Harga
        harga_display = f"Rp{int(prod['price']):,}" if prod.get('price') is not None else "Rp0"
        ctk.CTkLabel(card, text=harga_display, font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#003773").pack(pady=2)

    # --------------------------- UI: DETAIL & ADD TO CART ---------------------------
    def show_detail(self, prod):
        nama = prod['name']
        harga = prod['price']
        stock = prod.get('stock', 0)
        pid = prod.get('productid')

        detail = ctk.CTkToplevel(self)
        detail.title(nama)
        detail.geometry("500x700")
        detail.resizable(False, False)
        detail.grab_set()

        img_big = buat_placeholder((200, 200))
        ctk_img = ctk.CTkImage(light_image=img_big, size=(200, 200))
        lbl_gambar = ctk.CTkLabel(detail, image=ctk_img, text="")
        lbl_gambar.image = ctk_img
        lbl_gambar.pack(pady=(20, 10))

        ctk.CTkLabel(detail, text=nama, font=ctk.CTkFont(size=24, weight="bold"), wraplength=460, justify="center").pack(pady=(0, 10))
        ctk.CTkLabel(detail, text=f"Rp{int(harga):,}", font=ctk.CTkFont(size=28, weight="bold"), text_color="#003773").pack(pady=(0, 10))
        ctk.CTkLabel(detail, text=f"Stock: {stock}", font=ctk.CTkFont(size=14), text_color="#666666").pack(pady=(0, 10))

        frame_qty = ctk.CTkFrame(detail, fg_color="transparent")
        frame_qty.pack(pady=10)

        quantity = ctk.IntVar(value=1)

        def kurang():
            if quantity.get() > 1:
                quantity.set(quantity.get() - 1)
                update_add_button_state()

        def tambah():
            quantity.set(quantity.get() + 1)
            update_add_button_state()

        ctk.CTkButton(frame_qty, text="  –  ", width=40, font=ctk.CTkFont(size=20), command=kurang).pack(side="left", padx=10)
        ctk.CTkLabel(frame_qty, textvariable=quantity, font=ctk.CTkFont(size=22, weight="bold"), width=60).pack(side="left")
        ctk.CTkButton(frame_qty, text="  +  ", width=40, font=ctk.CTkFont(size=20), command=tambah).pack(side="left", padx=10)

        # add to cart button
        add_btn = ctk.CTkButton(
            detail,
            text="Masukkan Keranjang",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#ff6b00",
            hover_color="#e55a00",
            height=50,
            command=lambda: self.add_to_cart(pid, quantity.get(), detail)
        )
        add_btn.pack(pady=15, padx=50, fill="x")

        buy_now_btn = ctk.CTkButton(
            detail,
            text="Beli Sekarang",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#003773",
            hover_color="#1d4ed8",
            height=55,
            command=self.buka_checkout
        )
        buy_now_btn.pack(pady=(5, 30), padx=50, fill="x")

        def update_add_button_state():
            q = quantity.get()
            if stock <= 0 or q > stock:
                add_btn.configure(state="disabled")
            else:
                add_btn.configure(state="normal")

        update_add_button_state()

    def add_to_cart(self, productid, qty, parent_window=None):
        if not self.userid:
            CTkMessagebox(title="Error", message="Anda harus login untuk menambahkan ke keranjang", icon="warning")
            return

        try:
            # ensure product exists and has enough stock, and get unit price
            self.db.cursor.execute("SELECT price, quantity, productname FROM products WHERE productid=%s", (productid,))
            row = self.db.cursor.fetchone()
            if not row:
                CTkMessagebox(title="Error", message="Produk tidak ditemukan", icon="warning")
                return
            unit_price = float(row[0]) if row[0] is not None else 0
            stock = int(row[1]) if row[1] is not None else 0
            pname = row[2] if row[2] is not None else ""

            # get or create cart
            cartid = self.get_or_create_cart()

            # check existing quantity in cart for this product
            self.db.cursor.execute("SELECT detailid, quantity, price FROM detail WHERE cartid=%s AND productid=%s", (cartid, productid))
            r = self.db.cursor.fetchone()
            existing = int(r[1]) if r else 0

            if qty + existing > stock:
                CTkMessagebox(title="Error", message="Jumlah melebihi stock yang tersedia", icon="warning")
                return

            if r:
                # update detail: new quantity and new total price
                detailid = r[0]
                newq = existing + qty
                new_total = unit_price * newq
                self.db.cursor.execute("UPDATE detail SET quantity=%s, price=%s WHERE detailid=%s", (newq, new_total, detailid))
            else:
                # insert detail with total price (unit_price * qty)
                total_price = unit_price * qty
                self.db.cursor.execute(
                    "INSERT INTO detail (cartid, quantity, productid, price, productname) VALUES (%s, %s, %s, %s, %s)",
                    (cartid, qty, productid, total_price, pname)
                )

            self.db.db.commit()
            CTkMessagebox(title="Sukses", message="Produk berhasil dimasukkan ke keranjang", icon="check")
            if parent_window:
                parent_window.destroy()
        except Exception as e:
            # print full exception to console for debugging, show single consistent error popup
            print("add_to_cart error:", e)
            CTkMessagebox(title="Error", message="Terjadi kesalahan saat menambahkan ke keranjang", icon="cancel")

    # --------------------------- CART UI ---------------------------
    def open_cart(self):
        if not self.userid:
            CTkMessagebox(title="Error", message="Anda harus login untuk melihat keranjang", icon="warning")
            return

        cartid = self.get_or_create_cart()
        cart_win = ctk.CTkToplevel(self)
        cart_win.title("Keranjang Saya")
        cart_win.geometry("600x600")
        cart_win.grab_set()

        frame = ctk.CTkScrollableFrame(cart_win, fg_color="#ffffff")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # load cart details
        self.db.cursor.execute("SELECT detailid, productid, quantity, price, productname FROM detail WHERE cartid=%s", (cartid,))
        rows = self.db.cursor.fetchall()

        total = 0.0
        for r in rows:
            detailid, productid, quantity, price, productname = r
            item_frame = ctk.CTkFrame(frame, fg_color="#f8f8f8", corner_radius=8)
            item_frame.pack(fill="x", pady=6, padx=6)

            ctk.CTkLabel(item_frame, text=productname, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(6,0))

            # price in DB is total price (unit * quantity). compute unit safely
            unit_price = float(price) / int(quantity) if int(quantity) > 0 else float(price)
            # Display: unit x qty = total
            ctk.CTkLabel(item_frame, text=f"Rp{int(unit_price):,}  x {quantity}  =  Rp{int(price):,}", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)

            def make_change_func(did, pid):
                def change(qdelta):
                    # update quantity for detail
                    self.db.cursor.execute("SELECT quantity FROM detail WHERE detailid=%s", (did,))
                    cur = self.db.cursor.fetchone()
                    if not cur:
                        return
                    newq = int(cur[0]) + qdelta
                    if newq <= 0:
                        # remove item
                        self.db.cursor.execute("DELETE FROM detail WHERE detailid=%s", (did,))
                    else:
                        # ensure not exceed stock
                        self.db.cursor.execute("SELECT price, quantity FROM products WHERE productid=%s", (pid,))
                        pcur = self.db.cursor.fetchone()
                        if not pcur:
                            CTkMessagebox(title="Error", message="Produk tidak ditemukan", icon="warning")
                            return
                        unit = float(pcur[0]) if pcur[0] is not None else 0
                        stock = int(pcur[1]) if pcur[1] is not None else 0
                        if newq > stock:
                            CTkMessagebox(title="Error", message="Jumlah melebihi stock yang tersedia", icon="warning")
                            return
                        new_total = unit * newq
                        self.db.cursor.execute("UPDATE detail SET quantity=%s, price=%s WHERE detailid=%s", (newq, new_total, did))
                    self.db.db.commit()
                    cart_win.destroy()
                    self.open_cart()  # refresh
                return change

            btn_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            btn_frame.pack(anchor="e", pady=6, padx=10)
            ctk.CTkButton(btn_frame, text="–", width=40, command=lambda f=make_change_func(detailid, productid): f(-1)).pack(side="left", padx=6)
            ctk.CTkButton(btn_frame, text="+", width=40, command=lambda f=make_change_func(detailid, productid): f(1)).pack(side="left", padx=6)

            total += float(price)  # price is already total per line

        ctk.CTkLabel(cart_win, text=f"Total: Rp{int(total):,}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#00aa5b").pack(pady=10)

        ctk.CTkButton(cart_win, text="Checkout", font=ctk.CTkFont(size=16, weight="bold"), fg_color="#003773", hover_color="#1d4ed8", command=lambda: self.checkout(cartid, cart_win)).pack(pady=8, padx=40, fill="x")
        ctk.CTkButton(cart_win, text="Tutup", font=ctk.CTkFont(size=14), fg_color="#6b7280", command=cart_win.destroy).pack(pady=6, padx=40, fill="x")

    def checkout(self, cartid, window):
        try:
            # validate stock for all items
            self.db.cursor.execute("SELECT productid, quantity FROM detail WHERE cartid=%s", (cartid,))
            items = self.db.cursor.fetchall()
            for item in items:
                pid, q = item
                self.db.cursor.execute("SELECT quantity FROM products WHERE productid=%s", (pid,))
                r = self.db.cursor.fetchone()
                stock = int(r[0]) if r else 0
                if q > stock:
                    CTkMessagebox(title="Error", message=f"Produk (id {pid}) tidak cukup stock", icon="warning")
                    return
            # deduct stock
            for item in items:
                pid, q = item
                self.db.cursor.execute("UPDATE products SET quantity = quantity - %s WHERE productid=%s", (q, pid))
            # set checkout time
            now = datetime.now()
            self.db.cursor.execute("UPDATE cart SET checkout=%s WHERE cartid=%s", (now, cartid))
            self.db.db.commit()

            CTkMessagebox(title="Sukses", message="Pembayaran Berhasil!", icon="check")
            window.destroy()
            # refresh product list
            self.products = self.load_products()
            for widget in self.container.winfo_children():
                widget.destroy()
            for idx, prod in enumerate(self.products):
                self.create_product_card(self.container, idx, prod)
        except Exception as e:
            print("checkout error:", e)
            CTkMessagebox(title="Error", message="Terjadi kesalahan saat checkout", icon="cancel")

    # --------------------------- ACCOUNT / VENDOR MANAGEMENT ---------------------------
    def open_account_menu(self):
        menu = ctk.CTkToplevel(self)
        menu.title("Akun")
        menu.geometry("350x300")
        menu.grab_set()

        ctk.CTkLabel(menu, text=f"{self.username}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        ctk.CTkLabel(menu, text=f"Role: {self.role}", font=ctk.CTkFont(size=12)).pack(pady=6)

        if self.role == 'customer' or self.role is None:
            ctk.CTkButton(menu, text="Bergabung menjadi Vendor", fg_color="#003773", hover_color="#1d4ed8", command=lambda: self.become_vendor(menu)).pack(pady=8, padx=30, fill="x")
        else:
            ctk.CTkButton(menu, text="Kelola Toko", fg_color="#003773", hover_color="#1d4ed8", command=lambda: self.manage_store(menu)).pack(pady=8, padx=30, fill="x")

        ctk.CTkButton(menu, text="Logout", fg_color="#ba2f2f", command=lambda: self.logout(menu)).pack(pady=8, padx=30, fill="x")

    def logout(self, menu=None):
        try:
            for callback in self.tk.eval('after info').split():
                self.after_cancel(callback)
        except:
            pass

        if menu:
            menu.destroy()
        self.destroy()               # Close HomePage window

        import Login                 # Import login.py
        Login.App().mainloop()       # Restart login window

    def become_vendor(self, parent_menu=None):
        # ask for store name, create store, update role
        def create_store_action():
            name = entry.get().strip()
            if not name:
                CTkMessagebox(title="Error", message="Masukkan nama toko", icon="warning")
                return
            try:
                # insert store
                self.db.cursor.execute("INSERT INTO stores (userid, storename) VALUES (%s, %s)", (self.userid, name))
                # update role
                self.db.cursor.execute("UPDATE userdata SET roleuser='vendor' WHERE userid=%s", (self.userid,))
                self.db.db.commit()
                self.role = 'vendor'
                CTkMessagebox(title="Sukses", message="Anda sekarang vendor!", icon="check")
                popup.destroy()
                if parent_menu:
                    parent_menu.destroy()
            except Exception as e:
                print("become_vendor error:", e)
                CTkMessagebox(title="Error", message="Gagal membuat toko", icon="cancel")

        popup = ctk.CTkToplevel(self)
        popup.title("Buat Toko")
        popup.geometry("350x180")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Nama Toko", font=ctk.CTkFont(size=14)).pack(pady=10)
        entry = ctk.CTkEntry(popup, width=280)
        entry.pack(pady=6)
        ctk.CTkButton(popup, text="Buat Toko", command=create_store_action, fg_color="#003773").pack(pady=10)

    def manage_store(self, parent_menu=None):
        # open store management window
        try:
            self.db.cursor.execute("SELECT storeid, storename FROM stores WHERE userid=%s", (self.userid,))
            stores = self.db.cursor.fetchall()
        except Exception as e:
            print("manage_store error:", e)
            stores = []

        if not stores:
            CTkMessagebox(title="Info", message="Anda belum memiliki toko", icon="info")
            return

        storeid = stores[0][0]

        manage_win = ctk.CTkToplevel(self)
        manage_win.title("Kelola Toko")
        manage_win.geometry("800x600")
        manage_win.grab_set()

        header = ctk.CTkLabel(manage_win, text=f"Toko: {stores[0][1]}", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(pady=10)

        list_frame = ctk.CTkScrollableFrame(manage_win, fg_color="#ffffff")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # load products for this store (no description)
        try:
            self.db.cursor.execute("SELECT productid, productname, price, quantity FROM products WHERE storeid=%s", (storeid,))
            prods = self.db.cursor.fetchall()
        except Exception as e:
            print("manage_store load products error:", e)
            prods = []

        for p in prods:
            pid, pname, price, qty = p
            item_frame = ctk.CTkFrame(list_frame, fg_color="#f8f8f8", corner_radius=8)
            item_frame.pack(fill="x", pady=8, padx=8)

            name_entry = ctk.CTkEntry(item_frame, width=300)
            name_entry.insert(0, pname)
            name_entry.pack(side="left", padx=6)

            qty_entry = ctk.CTkEntry(item_frame, width=80)
            qty_entry.insert(0, str(qty))
            qty_entry.pack(side="left", padx=6)

            price_entry = ctk.CTkEntry(item_frame, width=120)
            price_entry.insert(0, str(int(price) if price is not None else 0))
            price_entry.pack(side="left", padx=6)

            def make_update_func(pid, name_e, qty_e, price_e):
                def update():
                    try:
                        newname = name_e.get().strip()
                        newqty = int(qty_e.get())
                        newprice = float(price_e.get())
                        self.db.cursor.execute("UPDATE products SET productname=%s, quantity=%s, price=%s WHERE productid=%s", (newname, newqty, newprice, pid))
                        self.db.db.commit()
                        CTkMessagebox(title="Sukses", message="Produk diperbarui", icon="check")
                    except Exception as e:
                        print("update product error:", e)
                        CTkMessagebox(title="Error", message="Gagal memperbarui produk", icon="cancel")
                return update

            ctk.CTkButton(item_frame, text="Simpan", command=make_update_func(pid, name_entry, qty_entry, price_entry)).pack(side="right", padx=6)

        # Add new product section (no description)
        add_frame = ctk.CTkFrame(manage_win, fg_color="#f3f3f3", corner_radius=8)
        add_frame.pack(fill="x", padx=10, pady=6)

        ctk.CTkLabel(add_frame, text="Tambah Produk Baru", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=8, pady=(6,2))

        # Nama Produk
        self.entry_nama_produk = ctk.CTkEntry(add_frame, width=300, placeholder_text="Masukkan nama produk")
        self.entry_nama_produk.pack(padx=8, pady=4, anchor="w")
        # Harga Produk
        self.entry_harga_produk = ctk.CTkEntry(add_frame, width=200, placeholder_text="Harga")
        self.entry_harga_produk.pack(padx=8, pady=4, anchor="w")
        # Stok Produk
        self.entry_stok_produk = ctk.CTkEntry(add_frame, width=120, placeholder_text="Jumlah stok")
        self.entry_stok_produk.pack(padx=8, pady=4, anchor="w")

        def add_product_action():
            try:
                pname = self.entry_nama_produk.get().strip()
                price = float(self.entry_harga_produk.get())
                qty = int(self.entry_stok_produk.get())
                if not pname:
                    CTkMessagebox(title="Error", message="Masukkan nama produk", icon="warning")
                    return
                # Insert without description column
                self.db.cursor.execute("INSERT INTO products (storeid, productname, price, quantity) VALUES (%s, %s, %s, %s)", (storeid, pname, price, qty))
                self.db.db.commit()
                CTkMessagebox(title="Sukses", message="Produk ditambahkan", icon="check")
                manage_win.destroy()
                # reopen manage_store to refresh (pass parent_menu so original caller can be closed if needed)
                self.manage_store(parent_menu)
            except Exception as e:
                print("add product error:", e)
                CTkMessagebox(title="Error", message="Gagal menambahkan produk", icon="cancel")

        ctk.CTkButton(add_frame, text="Tambah Produk", command=add_product_action, fg_color="#003773").pack(pady=8)



    # buka_checkout tersedia untuk "Beli Sekarang" dari detail, akan membuka cart checkout langsung
    def buka_checkout(self):
        # just open cart window (user can press Checkout button there)
        self.open_cart()


# Jalankan
if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
