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
    tx = "No Image"
    text_x = size[0] // 2 - (len(tx) * 4)
    text_y = size[1] // 2 - 10
    draw.text((text_x, text_y), tx, fill="#aaaaaa")
    return img


class HomePage(ctk.CTk):
    def __init__(self, username="User"):
        super().__init__()
        self.username = username
        self.db = Database()
        self._popup_open = False  # untuk mencegah double popup

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
        # kita simpan container sebagai attribute agar dapat di-refresh
        self.container = ctk.CTkScrollableFrame(self, fg_color="#f9f9f9")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # buat grid frame di dalam container agar kita bisa lock ukuran
        self.grid_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True)
        # stop propagation supaya ukuran tidak berubah otomatis (membantu mencegah loncat)
        self.grid_frame.pack_propagate(False)

        # columns konfigurasi (kita pakai grid pada grid_frame)
        for i in range(5):
            self.grid_frame.grid_columnconfigure(i, weight=1)

        # load products from DB
        self.products = self.load_products()

        # render initial products
        self.tampilkan_produk()

        # === BOTTOM NAVIGATION (Cart - Keluar - Akun) ===
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

        # Home center button (keluar)
        btn_home = ctk.CTkButton(
            bottom_nav, text="Keluar", width=100, height=50,
            fg_color="#003773", text_color="white", corner_radius=25,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.destroy()
        )
        btn_home.place(relx=0.5, rely=0.5, anchor="center")

        # Akun (ikon orang) with menu
        btn_profile = ctk.CTkButton(
            bottom_nav, text="Akun", width=80, fg_color="transparent",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#003773",
            hover_color="#f0f0f0", command=self.open_account_menu
        )
        btn_profile.place(x=350, y=25)

    # --------------------------- HELPERS ---------------------------
    def show_msg(self, title="Info", message="", icon="info"):
        """
        Wrapper untuk mencegah popup double. Menggunakan CTkMessagebox untuk familiaritas,
        tapi memastikan hanya satu popup terbuka pada satu waktu.
        """
        if self._popup_open:
            return
        try:
            self._popup_open = True
            CTkMessagebox(title=title, message=message, icon=icon)
        finally:
            self._popup_open = False

    # --------------------------- DATABASE HELPERS ---------------------------
    def load_products(self):
        products = []
        try:
            # select productid, productname, price, quantity, description
            self.db.cursor.execute("SELECT productid, productname, price, quantity, description FROM products")
            rows = self.db.cursor.fetchall()
            for r in rows:
                products.append({
                    "productid": r[0],
                    "name": r[1],
                    "price": float(r[2]) if r[2] is not None else 0,
                    "stock": int(r[3]) if r[3] is not None else 0,
                    "desc": r[4] or ""
                })
        except Exception as e:
            print("Failed to load products from DB, using fallback sample. Error:", e)
            # fallback sample
            products = [
                {"productid": 1, "name": "Sofa", "price": 100000, "stock": 2, "desc": "Sofa nyaman"},
                {"productid": 2, "name": "Lampu", "price": 25000, "stock": 0, "desc": "Lampu LED"},
                {"productid": 3, "name": "Meja", "price": 75000, "stock": 5, "desc": "Meja kayu"},
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
            # coba insert dengan kolom total jika ada; masih simpel -> biarkan DB handle default NULL jika kolom ada
            self.db.cursor.execute("INSERT INTO cart (userid, checkout) VALUES (%s, %s)", (self.userid, now))
            self.db.db.commit()
            # lastrowid mungkin tidak tersedia di semua DB adapters; gunakan cursor.lastrowid jika ada
            try:
                return self.db.cursor.lastrowid
            except Exception:
                # fallback: query kembali cart terbaru untuk userid
                self.db.cursor.execute("SELECT cartid FROM cart WHERE userid=%s AND checkout IS NULL ORDER BY cartid DESC LIMIT 1", (self.userid,))
                rr = self.db.cursor.fetchone()
                return rr[0] if rr else None
        except Exception as e:
            print("get_or_create_cart error:", e)
            return None

    # --------------------------- UI: PRODUCT DISPLAY ---------------------------
    def tampilkan_produk(self):
        """
        Render produk ke dalam grid_frame. Panggil hanya dari dalam class
        atau melalui refresh_produk().
        """
        for idx, prod in enumerate(self.products):
            self.create_product_card(self.grid_frame, idx, prod)

    def refresh_produk(self):
        """
        Hapus semua card lalu reload produk dari DB dan render ulang.
        Panggil setelah add/update/delete product.
        """
        # hapus semua widget di grid_frame
        for w in self.grid_frame.winfo_children():
            w.destroy()
        # reload product list dari DB
        self.products = self.load_products()
        # render ulang
        self.tampilkan_produk()

    def create_product_card(self, parent, idx, prod):
        row = idx // 5
        col = idx % 5

        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color="white",
            border_width=1,
            border_color="#eeeeee",
            width=220,
            height=320
        )
        card.grid(row=row, column=col, padx=10, pady=12, sticky="nsew")
        # stop card auto resizing (help reduce jumpiness)
        card.grid_propagate(False)
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

        # Stock
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
            self.show_msg(title="Error", message="Anda harus login untuk menambahkan ke keranjang", icon="warning")
            return

        try:
            # ensure product exists and has enough stock
            self.db.cursor.execute("SELECT quantity, price, productname FROM products WHERE productid=%s", (productid,))
            row = self.db.cursor.fetchone()
            if not row:
                self.show_msg(title="Error", message="Produk tidak ditemukan", icon="warning")
                return
            stock = int(row[0])
            price_per_unit = float(row[1]) if row[1] is not None else 0
            pname = row[2] if row[2] is not None else ""

            if qty <= 0:
                self.show_msg(title="Error", message="Jumlah harus lebih dari 0", icon="warning")
                return

            cartid = self.get_or_create_cart()
            if not cartid:
                self.show_msg(title="Error", message="Tidak dapat membuat atau menemukan keranjang", icon="warning")
                return

            # check existing quantity in cart for this product
            self.db.cursor.execute("SELECT detailid, quantity FROM detail WHERE cartid=%s AND productid=%s", (cartid, productid))
            r = self.db.cursor.fetchone()
            existing = int(r[1]) if r else 0

            if qty + existing > stock:
                self.show_msg(title="Error", message="Jumlah melebihi stock yang tersedia", icon="warning")
                return

            if r:
                # update detail (update quantity)
                newq = existing + qty
                self.db.cursor.execute("UPDATE detail SET quantity=%s WHERE detailid=%s", (newq, r[0]))
            else:
                # insert detail with price per unit and productname
                self.db.cursor.execute(
                    "INSERT INTO detail (cartid, quantity, productid, price, productname) VALUES (%s, %s, %s, %s, %s)",
                    (cartid, qty, productid, price_per_unit, pname)
                )

            self.db.db.commit()
            self.show_msg(title="Sukses", message="Produk berhasil dimasukkan ke keranjang", icon="check")
            # jangan destroy parent_window di sini, kita hanya close detail window jika ada
            if parent_window:
                parent_window.destroy()
        except Exception as e:
            print("add_to_cart error:", e)
            self.show_msg(title="Error", message="Terjadi kesalahan saat menambahkan ke keranjang", icon="cancel")

    # --------------------------- CART UI ---------------------------
    def open_cart(self):
        if not self.userid:
            self.show_msg(title="Error", message="Anda harus login untuk melihat keranjang", icon="warning")
            return

        cartid = self.get_or_create_cart()
        if not cartid:
            self.show_msg(title="Error", message="Tidak ada keranjang aktif", icon="warning")
            return

        # Buat window cart kalau belum ada, atau fokuskan jika sudah ada
        # Simpler: buat baru tiap kali user click Cart (window tetap stabil saat update qty)
        cart_win = ctk.CTkToplevel(self)
        cart_win.title("Keranjang Saya")
        cart_win.geometry("600x600")
        cart_win.grab_set()

        # frame konten (kita akan refresh isinya, bukan destroy window)
        content_frame = ctk.CTkFrame(cart_win, fg_color="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        content_frame.pack_propagate(False)

        # scrollable area for items
        items_frame = ctk.CTkScrollableFrame(content_frame, fg_color="#ffffff", height=420)
        items_frame.pack(fill="both", expand=False, padx=4, pady=4)

        # tempat total & tombol
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="#ffffff")
        bottom_frame.pack(fill="x", side="bottom", padx=4, pady=6)

        # buat fungsi untuk render isi keranjang (dipanggil ulang tiap update)
        def render_cart_contents():
            # hapus isi items_frame
            for w in items_frame.winfo_children():
                w.destroy()

            # ambil data detail
            try:
                self.db.cursor.execute("SELECT detailid, productid, quantity, price, productname FROM detail WHERE cartid=%s", (cartid,))
                rows = self.db.cursor.fetchall()
            except Exception as e:
                print("load cart detail error:", e)
                rows = []

            total = 0
            for r in rows:
                detailid, productid, quantity, price, productname = r
                item_frame = ctk.CTkFrame(items_frame, fg_color="#f8f8f8", corner_radius=8)
                item_frame.pack(fill="x", pady=6, padx=6)

                ctk.CTkLabel(item_frame, text=productname, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10, pady=(6,0))
                ctk.CTkLabel(item_frame, text=f"Rp{int(price):,}  x {quantity}", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10)

                def make_change_func(did, pid):
                    def change(qdelta):
                        try:
                            # ambil current
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
                                self.db.cursor.execute("SELECT quantity FROM products WHERE productid=%s", (pid,))
                                pcur = self.db.cursor.fetchone()
                                stock = int(pcur[0]) if pcur else 0
                                if newq > stock:
                                    self.show_msg(title="Error", message="Jumlah melebihi stock yang tersedia", icon="warning")
                                    return
                                self.db.cursor.execute("UPDATE detail SET quantity=%s WHERE detailid=%s", (newq, did))
                            self.db.db.commit()
                        except Exception as e:
                            print("change cart qty error:", e)
                            self.show_msg(title="Error", message="Gagal mengubah jumlah", icon="cancel")
                        # render ulang isi cart tapi jangan destroy window — menjaga posisi ukuran window
                        render_cart_contents()
                    return change

                btn_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                btn_frame.pack(anchor="e", pady=6, padx=10)
                ctk.CTkButton(btn_frame, text="–", width=40, command=lambda f=make_change_func(detailid, productid): f(-1)).pack(side="left", padx=6)
                ctk.CTkButton(btn_frame, text="+", width=40, command=lambda f=make_change_func(detailid, productid): f(1)).pack(side="left", padx=6)

                total += int(price) * int(quantity)

            # update total label (hapus lalu buat ulang agar mudah)
            for w in bottom_frame.winfo_children():
                w.destroy()

            ctk.CTkLabel(bottom_frame, text=f"Total: Rp{total:,}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#00aa5b").pack(pady=10)
            ctk.CTkButton(bottom_frame, text="Checkout", font=ctk.CTkFont(size=16, weight="bold"), fg_color="#003773", hover_color="#1d4ed8", command=lambda: self.checkout(cartid, cart_win)).pack(pady=8, padx=40, fill="x")
            ctk.CTkButton(bottom_frame, text="Tutup", font=ctk.CTkFont(size=14), fg_color="#6b7280", command=cart_win.destroy).pack(pady=6, padx=40, fill="x")

        # initial render
        render_cart_contents()

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
                    self.show_msg(title="Error", message=f"Produk (id {pid}) tidak cukup stock", icon="warning")
                    return

            # deduct stock
            for item in items:
                pid, q = item
                self.db.cursor.execute("UPDATE products SET quantity = quantity - %s WHERE productid=%s", (q, pid))

            # compute total from detail (quantity * price)
            self.db.cursor.execute("SELECT SUM(quantity * price) FROM detail WHERE cartid=%s", (cartid,))
            total_row = self.db.cursor.fetchone()
            total_amount = float(total_row[0]) if total_row and total_row[0] is not None else 0.0

            # set checkout time
            now = datetime.now()
            # try update cart with total (if kolom total tidak ada, ignore)
            try:
                self.db.cursor.execute("UPDATE cart SET checkout=%s, total=%s WHERE cartid=%s", (now, total_amount, cartid))
            except Exception:
                # fallback: hanya update checkout jika kolom total tidak ada
                self.db.cursor.execute("UPDATE cart SET checkout=%s WHERE cartid=%s", (now, cartid))

            self.db.db.commit()

            self.show_msg(title="Sukses", message="Pembayaran Berhasil!", icon="check")
            window.destroy()
            # refresh product list di UI agar stock terbaru tampil
            self.refresh_produk()
        except Exception as e:
            print("checkout error:", e)
            self.show_msg(title="Error", message="Terjadi kesalahan saat checkout", icon="cancel")

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

    def become_vendor(self, parent_menu=None):
        def create_store_action():
            name = entry.get().strip()
            if not name:
                self.show_msg(title="Error", message="Masukkan nama toko", icon="warning")
                return
            try:
                # insert store
                self.db.cursor.execute("INSERT INTO stores (userid, storename) VALUES (%s, %s)", (self.userid, name))
                # update role
                self.db.cursor.execute("UPDATE userdata SET roleuser='vendor' WHERE userid=%s", (self.userid,))
                self.db.db.commit()
                self.role = 'vendor'
                self.show_msg(title="Sukses", message="Anda sekarang vendor!", icon="check")
                popup.destroy()
                if parent_menu:
                    parent_menu.destroy()
            except Exception as e:
                print("become_vendor error:", e)
                self.show_msg(title="Error", message="Gagal membuat toko", icon="cancel")

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
            self.show_msg(title="Info", message="Anda belum memiliki toko", icon="info")
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

        # load products for this store
        try:
            self.db.cursor.execute("SELECT productid, productname, description, price, quantity FROM products WHERE storeid=%s", (storeid,))
            prods = self.db.cursor.fetchall()
        except Exception as e:
            print("manage_store load products error:", e)
            prods = []

        for p in prods:
            pid, pname, pdesc, price, qty = p
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
                        self.show_msg(title="Sukses", message="Produk diperbarui", icon="check")
                        # refresh main product list
                        self.refresh_produk()
                    except Exception as e:
                        print("update product error:", e)
                        self.show_msg(title="Error", message="Gagal memperbarui produk", icon="cancel")
                return update

            ctk.CTkButton(item_frame, text="Simpan", command=make_update_func(pid, name_entry, qty_entry, price_entry)).pack(side="right", padx=6)

        # Add new product section
        add_frame = ctk.CTkFrame(manage_win, fg_color="#f3f3f3", corner_radius=8)
        add_frame.pack(fill="x", padx=10, pady=6)

        ctk.CTkLabel(add_frame, text="Tambah Produk Baru", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=8, pady=(6,2))

        # Nama Produk
        self.entry_nama_produk = ctk.CTkEntry(add_frame, width=300, placeholder_text="Masukkan nama produk")
        self.entry_nama_produk.pack(padx=8, pady=4, anchor="w")
        # Deskripsi Produk
        self.entry_deskripsi_produk = ctk.CTkEntry(add_frame, width=500, placeholder_text="Masukkan deskripsi produk")
        self.entry_deskripsi_produk.pack(padx=8, pady=4, anchor="w")
        # Harga Produk
        self.entry_harga_produk = ctk.CTkEntry(add_frame, width=200, placeholder_text="Harga")
        self.entry_harga_produk.pack(padx=8, pady=4, anchor="w")
        # Stok Produk
        self.entry_stok_produk = ctk.CTkEntry(add_frame, width=120, placeholder_text="Jumlah stok")
        self.entry_stok_produk.pack(padx=8, pady=4, anchor="w")

        def add_product_action():
            try:
                pname = self.entry_nama_produk.get().strip()
                pdesc = self.entry_deskripsi_produk.get().strip()
                price = float(self.entry_harga_produk.get())
                qty = int(self.entry_stok_produk.get())
                if not pname:
                    self.show_msg(title="Error", message="Masukkan nama produk", icon="warning")
                    return
                self.db.cursor.execute("INSERT INTO products (storeid, productname, description, price, quantity) VALUES (%s, %s, %s, %s, %s)", (storeid, pname, pdesc, price, qty))
                self.db.db.commit()
                self.show_msg(title="Sukses", message="Produk ditambahkan", icon="check")
                manage_win.destroy()
                # refresh main product list agar item baru muncul otomatis
                self.refresh_produk()
                # reopen manage_store if you want to keep managing (optional)
                # self.manage_store(parent_menu)
            except Exception as e:
                print("add product error:", e)
                self.show_msg(title="Error", message="Gagal menambahkan produk", icon="cancel")

        ctk.CTkButton(add_frame, text="Tambah Produk", command=add_product_action, fg_color="#003773").pack(pady=8)

    def logout(self, menu_window=None):
        if menu_window:
            menu_window.destroy()
        self.destroy()

    # buka_checkout tersedia untuk "Beli Sekarang" dari detail, akan membuka cart checkout langsung
    def buka_checkout(self):
        # just open cart window (user can press Checkout button there)
        self.open_cart()


# Jalankan
if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
