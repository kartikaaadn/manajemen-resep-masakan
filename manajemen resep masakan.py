import csv
import tkinter as tk
from tkinter import messagebox, filedialog

class Resep:
    def __init__(self, nama, bahan, instruksi):
        self.nama = nama
        self.bahan = bahan
        self.instruksi = instruksi

    def __repr__(self):
        return f"Resep(nama={self.nama}, bahan={self.bahan}, instruksi={self.instruksi})"

class ManajemenResep:
    def __init__(self, file_path='resep.csv'):
        self.daftar_resep = []
        self.file_path = file_path
        self.impor_csv(self.file_path)

    def tambah_resep(self, resep):
        self.daftar_resep.append(resep)
        self.simpan_csv(self.file_path) 

    def lihat_resep(self):
        return self.daftar_resep

    def perbarui_resep(self, index, resep_baru):
        if 0 <= index < len(self.daftar_resep):
            self.daftar_resep[index] = resep_baru
            self.simpan_csv(self.file_path)  
            return True
        return False

    def hapus_resep(self, index):
        if 0 <= index < len(self.daftar_resep):
            del self.daftar_resep[index]
            self.simpan_csv(self.file_path)
            return True
        return False

    def cari_resep(self, keyword):
        hasil = [resep for resep in self.daftar_resep if keyword.lower() in resep.nama.lower() or keyword.lower() in resep.bahan.lower()]
        return hasil

    def urutkan_resep(self, kriteria="nama"):
        if kriteria == "nama":
            self.daftar_resep.sort(key=lambda resep: resep.nama)
        elif kriteria == "durasi":
            self.daftar_resep.sort(key=lambda resep: resep.durasi)

    def impor_csv(self, file_path):
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',', quotechar='"')
                next(reader, None) 
                self.daftar_resep = [Resep(row[0], row[1], row[2]) for row in reader]
        except FileNotFoundError:
            pass  

    def simpan_csv(self, file_path):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Nama Makanan', 'Bahan', 'Instruksi'])  
            for resep in self.daftar_resep:
                writer.writerow([resep.nama, resep.bahan, resep.instruksi])

    def perbarui_instruksi_resep(self, index, instruksi_baru):
        if 0 <= index < len(self.daftar_resep):
            self.daftar_resep[index].instruksi = instruksi_baru
            self.simpan_csv(self.file_path)  
            return True
        return False
class ManajemenResepApp:
    def _init_(self, root):
        self.manajemen_resep = ManajemenResep()
        self.root = root
        self.root.title("Sistem Manajemen Resep Masakan")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10, padx=10)

        self.label = tk.Label(self.frame, text="Welcome to Sistem Manajemen Resep Masakan", font=("Helvetica", 16))
        self.label.grid(row=0, columnspan=5, pady=10)

        self.btn_tambah = tk.Button(self.frame, text="Tambah Resep", command=self.tambah_resep, bg="light blue")
        self.btn_tambah.grid(row=1, column=0, padx=5, pady=5)

        self.btn_lihat = tk.Button(self.frame, text="Lihat Resep", command=self.lihat_resep, bg="light blue")
        self.btn_lihat.grid(row=1, column=1, padx=5, pady=5)

        self.btn_cari = tk.Button(self.frame, text="Cari Resep", command=self.cari_resep, bg="light blue")
        self.btn_cari.grid(row=1, column=2, padx=5, pady=5)

        self.btn_impor = tk.Button(self.frame, text="Impor CSV", command=self.impor_csv, bg="light blue")
        self.btn_impor.grid(row=1, column=3, padx=5, pady=5)

        self.btn_perbarui_instruksi = tk.Button(self.frame, text="Perbarui Instruksi Resep", command=self.perbarui_instruksi_resep, bg="light blue")
        self.btn_perbarui_instruksi.grid(row=1, column=4, padx=5, pady=5)

    def tambah_resep(self):
        top = tk.Toplevel(self.root)
        top.title("Tambah Resep")

        tk.Label(top, text="Nama:").pack(pady=5)
        entry_nama = tk.Entry(top)
        entry_nama.pack(pady=5)

        tk.Label(top, text="Bahan:").pack(pady=5)
        entry_bahan = tk.Text(top, height=3, wrap=tk.WORD)
        entry_bahan.pack(pady=5)

        tk.Label(top, text="Instruksi:").pack(pady=5)
        entry_instruksi = tk.Text(top, height=5, width=50)
        entry_instruksi.pack(pady=5)

        def simpan_resep():
            nama = entry_nama.get()
            bahan = entry_bahan.get("1.0", tk.END).strip()
            instruksi = entry_instruksi.get("1.0", tk.END).strip()
            resep = Resep(nama, bahan, instruksi)
            self.manajemen_resep.tambah_resep(resep)
            messagebox.showinfo("Info", "Resep berhasil ditambahkan")
            top.destroy()

        btn_simpan = tk.Button(top, text="Simpan", command=simpan_resep, bg="light blue")
        btn_simpan.pack(pady=5)
