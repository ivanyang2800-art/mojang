import customtkinter as ctk
from PIL import Image
import os

#Theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

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
            ("nama", "Rp57.500", "img1.png"),
            ("n", "Rp61.513", "img2.png"),
            ("n", "Rp948.999", "img3.png"),
            ("n", "Rp50.500","img4.png"),
            ("n", "Rp69.000","img5.png"),
            ("n", "Rp30.000", "img6.png"),
            ("n", "Rp68.899", "img7.png"),
            ("n", "Rp28.899", "img8.png"),
            ("n", "Rp1.275.000", "img9.png"),
            ("n", "Rp357.000", "img10.png"),
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

        # Home (tengah, lebih menonjol)
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

    def create_product_card(self, idx, nama, harga, img_path):
        row=idx // 5
        col=idx % 5

        # kartu produk
        card = ctk.CTkFrame(
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
            ctk_img = ctk.CTkImage(light_image=img, size=(180, 180))
            lbl_img = ctk.CTkLabel(card, image=ctk_img, text="")
            lbl_img.image = ctk_img  # keep reference
        except:
            lbl_img = ctk.CTkLabel(card, text="No Image", width=180, height=180, fg_color="#f0f0f0")
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
        detail.geometry("400x600")
        ctk.CTkLabel(detail, text=nama, font=ctk.CTkFont(size=20, weight="bold")).pack(pady=30)
        ctk.CTkLabel(detail, text=harga, font=ctk.CTkFont(size=24, weight="bold"), text_color="#00aa5b").pack(pady=10)
        ctk.CTkButton(detail, text="Beli Sekarang", fg_color="#00aa5b", height=50).pack(pady=50, fill="x", padx=40)

# Jalankan
if __name__ == "__main__":
    app = HomePage()
    app.mainloop()