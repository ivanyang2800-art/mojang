import customtkinter as ctk
from PIL import Image, ImageDraw
from CTkMessagebox import CTkMessagebox
from database import Database

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

keranjang = []
db = Database()  # pake database

def buat_placeholder(size=(180,180)):
    img = Image.new("RGB", size, "#f5f5f5")
    draw = ImageDraw.Draw(img)
    for i in range(-200, 400, 60):
        draw.line([(i,0),(i+180,180)], "#e0e0e0", 30)
        draw.line([(0,i),(180,i+180)], "#e0e0e0", 30)
        i += 60
    draw.text((50,80), "No Image", fill="#999")
    return img

class HomePage(ctk.CTk):
    def __init__(self, master=None, username="User"):
        super().__init__()
        self.master = master
        self.username = username
        self.title("UIB MART - Home")
        self.geometry("1200x800")

        ctk.CTkLabel(self, text=f"Halo, {username}!", font=ctk.CTkFont(size=32, weight="bold")).pack(pady=40)

        # Header
        header = ctk.CTkFrame(self, height=90, fg_color="white")
        header.pack(fill="x"); header.pack_propagate(False)
        ctk.CTkLabel(header, text="UIB MART", font=ctk.CTkFont(size=28, weight="bold"), text_color="#003773").place(x=30,y=25)
        ctk.CTkLabel(header, text="INSTAN BATAM", font=ctk.CTkFont(size=14), text_color="gray").place(x=30,y=60)

        # Produk dari database
        container = ctk.CTkScrollableFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=10)
        for i in range(5): container.grid_columnconfigure(i, weight=1)

        produk_dari_db = db.get_all_produk()
        for idx, (nama, harga, stok, gambar) in enumerate(produk_dari_db):
            self.bikin_card(container, idx, nama, f"Rp{harga:,}".replace(",","."), stok, gambar)

        # Tombol Keranjang
        ctk.CTkButton(self, text="Keranjang", width=160, height=55, fg_color="#ff6b00",
                       font=ctk.CTkFont(size=18, weight="bold"), command=self.lihat_keranjang).pack(side="bottom", pady=25)

    def bikin_card(self, parent, idx, nama, harga, stok, img_path):
        row, col = divmod(idx, 5)
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color="white")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.bind("<Button-1>", lambda e: self.detail_produk(nama, harga, stok, img_path))

        try:
            img = Image.open(img_path).resize((180,180), Image.Resampling.LANCZOS)
        except:
            img = buat_placeholder()
        ctk.CTkImage(light_image=img, size=(180,180))
        ctk.CTkLabel(card, image=ctk.CTkImage(light_image=img, size=(180,180)), text="").pack(pady=8)
        ctk.CTkLabel(card, text=nama, font=ctk.CTkFont(size=14, weight="bold")).pack()
        ctk.CTkLabel(card, text=harga, font=ctk.CTkFont(size=16, weight="bold"), text_color="#00aa5b").pack()
        ctk.CTkLabel(card, text=f"Stok: {stok}", font=ctk.CTkFont(size=12), text_color="gray").pack(pady=(0,10))

    def detail_produk(self, nama, harga, stok, img_path):
        win = ctk.CTkToplevel(self)
        win.title(nama); win.geometry("500x750"); win.grab_set()

        try:
            img = Image.open(img_path).resize((450,450), Image.Resampling.LANCZOS)
        except:
            img = buat_placeholder((450,450))
        ctk.CTkLabel(win, image=ctk.CTkImage(light_image=img, size=(450,450)), text="").pack(pady=20)

        ctk.CTkLabel(win, text=nama, font=ctk.CTkFont(size=26, weight="bold")).pack(pady=10)
        ctk.CTkLabel(win, text=harga, font=ctk.CTkFont(size=30, weight="bold"), text_color="#00aa5b").pack(pady=10)
        ctk.CTkLabel(win, text=f"Stok tersisa: {stok}", font=ctk.CTkFont(size=16)).pack(pady=10)

        qty = ctk.IntVar(value=1)
        frame = ctk.CTkFrame(win); frame.pack(pady=20)
        ctk.CTkButton(frame, text="–", width=50, command=lambda: qty.set(max(1,qty.get()-1))).pack(side="left", padx=10)
        ctk.CTkLabel(frame, textvariable=qty, font=ctk.CTkFont(size=24, weight="bold"), width=80).pack(side="left")
        ctk.CTkButton(frame, text="+", width=50, command=lambda: qty.set(qty.get()+1)).pack(side="left", padx=10)

        ctk.CTkButton(win, text="Masukkan Keranjang", fg_color="#ff6b00", height=50,
                       command=lambda: self.tambah_keranjang(nama, harga, qty.get(), stok, win)).pack(pady=20, fill="x", padx=50)

    def tambah_keranjang(self, nama, harga, qty, stok_tersedia, window):
        if qty > stok_tersedia:
            CTkMessagebox(title="Stok Habis", message=f"Hanya ada {stok_tersedia} stok!", icon="cancel")
            return

        # Kurangi stok di database
        db.kurangi_stok(nama, qty)

        # Tambah ke keranjang
        for item in keranjang:
            if item["nama"] == nama:
                item["qty"] += qty
                CTkMessagebox(message=f"{nama} +{qty} masuk keranjang!")
                window.destroy()
                return
        keranjang.append({"nama": nama, "harga": int(harga.replace("Rp","").replace(".","")), "qty": qty})
        CTkMessagebox(message=f"{nama} masuk keranjang!")
        window.destroy()

    def lihat_keranjang(self):
        if not keranjang:
            CTkMessagebox(message="Keranjang kosong!")
            return
        win = ctk.CTkToplevel(self)
        win.title("Keranjang")
        win.geometry("500x600")
        total = sum(item["harga"] * item["qty"] for item in keranjang)
        for item in keranjang:
            ctk.CTkLabel(win, text=f"{item['nama']} × {item['qty']} - Rp{item['harga']*item['qty']:,}".replace(",",".")).pack(pady=5)
        ctk.CTkLabel(win, text=f"TOTAL: Rp{total:,}".replace(",","."), font=ctk.CTkFont(size=24, weight="bold"), text_color="green").pack(pady=30)
        ctk.CTkButton(win, text="Checkout", fg_color="green", command=win.destroy).pack(pady=20, fill="x", padx=50)

if __name__ == "__main__":
    root = ctk.CTk()
    HomePage(root, username="Admin").mainloop()