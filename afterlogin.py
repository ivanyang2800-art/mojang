import customtkinter as ctk
from PIL import Image, ImageDraw
import os

#Theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def buat_placeholder(size=(180, 180)):
    img = Image.new("RGB", size, "#f0f0f0")
    draw = ImageDraw.Draw(img)
    for i in range(-size[0], size[1]*2, 40):
        draw.line([(i, 0), (i + size[1], size[1])], fill="#e0e0e0", width=20)
        draw.line([(0, i), (size[0], i + size[0])], fill="#e0e0e0", width=20)
    draw.text((size[0]//2 - 45, size[1]//2 - 15), "No Image", fill="#aaaaaa", font_size=20)
    
    return img

class HomePage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UIB MART")
        self.geometry("1000x640")
        self.resizable(False, False)
        self.state("zoomed")
        # self.iconbitmap("logo.ico")

        # === HEADER (Judul + lokasi) ===
        header = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#ffffff")
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="UIB MART",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="#00aa5b"
        ).place(x=20, y=30)

        ctk.CTkLabel(
            header,
            text="INSTAN BATAM",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        ).place(x=20, y=60)

        # === SCROLLABLE PRODUCT GRID ===
        container = ctk.CTkScrollableFrame(self, fg_color="#f9f9f9")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # 2 kolom grid
        for i in range(5):
            container.grid_columnconfigure(i, weight=1)

        # Daftar produk (nama, harga, path gambar)
        self.products = [
            ("Sofa", "Rp100.000", "img/img1.png"),
            ("n", "Rp0", "img2.png"),
            ("n", "Rp0", "img3.png"),
            ("n", "Rp0","img4.png"),
            ("n", "Rp0","img5.png"),
        ]

        for idx, (nama, harga, img_path) in enumerate(self.products):
            self.create_product_card(container, idx, nama, harga, img_path)

        # === BOTTOM NAVIGATION (Inbox - Home - Akun) ===
        bottom_nav = ctk.CTkFrame(self, height=80, fg_color="white", corner_radius=0)
        bottom_nav.pack(fill="x", side="bottom")
        bottom_nav.pack_propagate(False)

        # Inbox
        btn_inbox = ctk.CTkButton(
            bottom_nav, text="Inbox", width=80, fg_color="transparent",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#999999",
            hover_color="#f0f0f0", command=lambda: print("Inbox dibuka")
        )
        btn_inbox.place(x=60, y=25)

        # Home
        btn_home = ctk.CTkButton(
            bottom_nav, text="Home", width=100, height=50,
            fg_color="#00aa5b", text_color="white", corner_radius=25,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: print("Sudah di Home")
        )
        btn_home.place(relx=0.5, rely=0.5, anchor="center")

        # Akun (ikon orang)
        btn_profile = ctk.CTkButton(
            bottom_nav, text="Akun", width=80, fg_color="transparent",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#00aa5b",
            hover_color="#f0f0f0", command=lambda: print("Buka Profile")
        )
        btn_profile.place(x=340, y=25)

    def create_product_card(self,parent,idx, nama, harga, img_path):
        row=idx // 5
        col=idx % 5

        # kartu produk
        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color="white",
            border_width=1,
            border_color="#eeeeee"
        )
        card.grid(row=row, column=col, padx=10, pady=12, sticky="nsew")
        card.bind("<Button-1>", lambda e: self.show_detail(nama, harga))

        # Gambar produk
        try:
            img = Image.open(img_path).resize((180, 180), Image.Resampling.LANCZOS)
        except:
            img = buat_placeholder()
        ctk_img = ctk.CTkImage(light_image=img, size=(180, 180))
        lbl_img = ctk.CTkLabel(card, image=ctk_img, text="")
        lbl_img.image = ctk_img
        lbl_img.pack(pady=8)

        # Nama produk
        ctk.CTkLabel(card, text=nama, font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#222222", wraplength=170, justify="center").pack(pady=5)

        # Harga
        ctk.CTkLabel(card, text=harga, font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#00aa5b").pack(pady=2)

    def show_detail(self, nama, harga):
        detail = ctk.CTkToplevel(self)
        detail.title(nama)
        detail.geometry("500x700")
        detail.resizable(False, False)
        detail.grab_set()
        try:
            img_big = Image.open("img/img1.png").resize((450, 450), Image.Resampling.LANCZOS)
        except:
            img_big = self.buat_placeholder((200, 200))
        ctk_img = ctk.CTkImage(light_image=img_big, size=(200, 200))
        lbl_gambar = ctk.CTkLabel(detail, image=ctk_img, text="")
        lbl_gambar.image = ctk_img
        lbl_gambar.pack(pady=(20, 10))
        # === NAMA PRODUK ===
        ctk.CTkLabel(
            detail,
            text=nama,
            font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=460,
            justify="center"
        ).pack(pady=(0, 10))

        # === HARGA ===
        ctk.CTkLabel(
            detail,
            text=harga,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00aa5b"
        ).pack(pady=(0, 20))

        # === QUANTITY (+ / -) ===
        frame_qty = ctk.CTkFrame(detail, fg_color="transparent")
        frame_qty.pack(pady=10)

        quantity = ctk.IntVar(value=1)

        def kurang():
            if quantity.get() > 1:
                quantity.set(quantity.get() - 1)

        def tambah():
            quantity.set(quantity.get() + 1)

        ctk.CTkButton(frame_qty, text="  –  ", width=40, font=ctk.CTkFont(size=20),
                    command=kurang).pack(side="left", padx=10)
        
        ctk.CTkLabel(frame_qty, textvariable=quantity, font=ctk.CTkFont(size=22, weight="bold"), width=60).pack(side="left")
        
        ctk.CTkButton(frame_qty, text="  +  ", width=40, font=ctk.CTkFont(size=20),
                    command=tambah).pack(side="left", padx=10)

        # === TOMBOL BELI & KERANJANG ===
        ctk.CTkButton(
            detail,
            text="Masukkan Keranjang",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#ff6b00",
            hover_color="#e55a00",
            height=50,
            command=lambda: print(f"Keranjang: {nama} x{quantity.get()}")  # nanti diganti ke fungsi keranjang beneran
        ).pack(pady=15, padx=50, fill="x")

        ctk.CTkButton(
            detail,
            text="Beli Sekarang",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#00aa5b",
            hover_color="#00994d",
            height=55,
            command=lambda: print(f"Beli langsung: {nama} x{quantity.get()}")
        ).pack(pady=(5, 30), padx=50, fill="x")
# Jalankan
if __name__ == "__main__":
    app = HomePage()
    app.mainloop()