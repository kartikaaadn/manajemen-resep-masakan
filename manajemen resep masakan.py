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
        self.impor_csv(self.file_path)  # Auto-import CSV data upon initialization

    def tambah_resep(self, resep):
        self.daftar_resep.append(resep)
        self.simpan_csv(self.file_path)  # Save to CSV every time a new recipe is added

    def lihat_resep(self):
        return self.daftar_resep

    def perbarui_resep(self, index, resep_baru):
        if 0 <= index < len(self.daftar_resep):
            self.daftar_resep[index] = resep_baru
            self.simpan_csv(self.file_path)  # Save to CSV after updating
            return True
        return False

    def hapus_resep(self, index):
        if 0 <= index < len(self.daftar_resep):
            del self.daftar_resep[index]
            self.simpan_csv(self.file_path)  # Save to CSV after deleting
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
                next(reader, None)  # Skip the header
                self.daftar_resep = [Resep(row[0], row[1], row[2]) for row in reader]
        except FileNotFoundError:
            pass  # Ignore if the file does not exist

    def simpan_csv(self, file_path):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Nama Makanan', 'Bahan', 'Instruksi'])  # Write the header
            for resep in self.daftar_resep:
                writer.writerow([resep.nama, resep.bahan, resep.instruksi])

    def perbarui_instruksi_resep(self, index, instruksi_baru):
        if 0 <= index < len(self.daftar_resep):
            self.daftar_resep[index].instruksi = instruksi_baru
            self.simpan_csv(self.file_path)  # Save to CSV after updating instructions
            return True
        return False
