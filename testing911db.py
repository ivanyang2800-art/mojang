# database.py — versi MySQL (root + no password) — 100% JALAN
import mysql.connector
from CTkMessagebox import CTkMessagebox

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",           # kosong
                database="uibmart"
            )
            self.cursor = self.conn.cursor()
            self.buat_tabel()
        except Exception as e:
            CTkMessagebox(title="Koneksi Gagal", message=f"MySQL Error:\n{e}", icon="cancel")
            exit()

    def buat_tabel(self):
        # Pastikan database ada
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS uibmart")
        self.cursor.execute("USE uibmart")

        # Tabel user
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                password VARCHAR(100)
            )
        """)

        # Tabel produk
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produk (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100),
                harga INT,
                stok INT,
                gambar VARCHAR(200)
            )
        """)

        # Isi contoh produk kalau kosong
        self.cursor.execute("SELECT COUNT(*) FROM produk")
        if self.cursor.fetchone()[0] == 0:
            data = [
                ("Sofa Minimalis", 1250000, 10, "img/img1.jpg"),
                ("Kursi Gaming",   850000,  7, "img/img2.jpg"),
                ("Meja Belajar",   650000, 15, "img/img3.jpg"),
                ("Lemari Baju",    2100000, 5, "img/img4.jpg"),
                ("Kasur Springbed",3500000, 3, "img/img5.jpg"),
            ]
            self.cursor.executemany("INSERT INTO produk (nama, harga, stok, gambar) VALUES (%s, %s, %s, %s)", data)
            self.conn.commit()

    # FUNGSI YANG HARUS ADA INI!
    def get_all_produk(self):
        self.cursor.execute("SELECT nama, harga, stok, gambar FROM produk")
        return self.cursor.fetchall()

    def kurangi_stok(self, nama, qty):
        self.cursor.execute("UPDATE produk SET stok = stok - %s WHERE nama=%s", (qty, nama))
        self.conn.commit()

    def check_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        return self.cursor.fetchone()

    def create_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
            return True
        except:
            return False

    def __del__(self):
        self.conn.close()