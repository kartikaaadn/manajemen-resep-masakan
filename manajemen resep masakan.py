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
                next(reader, None)  # Skip the header
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
    def __init__(self, root):
        self.manajemen_resep = ManajemenResep()
        self.root = root
        self.root.title("Sistem Manajemen Resep Masakan")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10, padx=10)

        self.label = tk.Label(self.frame, text="Welcome to Sistem Manajemen Resep Masakan", font=("Helvetica", 16))
        self.label.grid(row=0, columnspan=7, pady=10)

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

        self.btn_perbarui_resep = tk.Button(self.frame, text="Perbarui Resep", command=self.perbarui_resep, bg="light blue")
        self.btn_perbarui_resep.grid(row=1, column=5, padx=5, pady=5)

        self.btn_hapus_resep = tk.Button(self.frame, text="Hapus Resep", command=self.hapus_resep, bg="light blue")
        self.btn_hapus_resep.grid(row=1, column=6, padx=5, pady=5)

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

    def lihat_resep(self):
        top = tk.Toplevel(self.root)
        top.title("Daftar Resep")

        text_widget = tk.Text(top, wrap=tk.WORD)
        text_widget.pack(expand=True, fill=tk.BOTH)

        daftar_resep = self.manajemen_resep.lihat_resep()
        for resep in daftar_resep:
            text_widget.insert(tk.END, f"Nama: {resep.nama}\n")
            text_widget.insert(tk.END, f"Bahan: {resep.bahan}\n")
            text_widget.insert(tk.END, f"Instruksi: {resep.instruksi}\n")
            text_widget.insert(tk.END, "\n" + "-"*40 + "\n\n")

        text_widget.config(state=tk.DISABLED)

    def cari_resep(self):
        top = tk.Toplevel(self.root)
        top.title("Cari Resep")

        tk.Label(top, text="Masukkan keyword:").pack(pady=5)
        entry_keyword = tk.Entry(top)
        entry_keyword.pack(pady=5)

        def cari():
            keyword = entry_keyword.get()
            hasil = self.manajemen_resep.cari_resep(keyword)
            hasil_window = tk.Toplevel(top)
            hasil_window.title("Hasil Pencarian")
            text_widget = tk.Text(hasil_window, wrap=tk.WORD)
            text_widget.pack(expand=True, fill=tk.BOTH)
            for resep in hasil:
                text_widget.insert(tk.END, f"Nama: {resep.nama}\n")
                text_widget.insert(tk.END, f"Bahan: {resep.bahan}\n")
                text_widget.insert(tk.END, f"Instruksi: {resep.instruksi}\n")
                text_widget.insert(tk.END, "\n" + "-"*40 + "\n\n")
            text_widget.config(state=tk.DISABLED)

        btn_cari = tk.Button(top, text="Cari", command=cari, bg="light blue")
        btn_cari.pack(pady=5)

    def impor_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.manajemen_resep.impor_csv(file_path)
            messagebox.showinfo("Info", "Data berhasil diimpor")

    def perbarui_instruksi_resep(self):
        top = tk.Toplevel(self.root)
        top.title("Perbarui Instruksi Resep")

        tk.Label(top, text="Indeks Resep:").pack(pady=5)
        entry_indeks = tk.Entry(top)
        entry_indeks.pack(pady=5)

        tk.Label(top, text="Instruksi Baru:").pack(pady=5)
        entry_instruksi_baru = tk.Text(top, height=5, width=50)
        entry_instruksi_baru.pack(pady=5)

        def update_instruksi():
            try:
                indeks = int(entry_indeks.get())
                instruksi_baru = entry_instruksi_baru.get("1.0", tk.END).strip()
                if self.manajemen_resep.perbarui_instruksi_resep(indeks, instruksi_baru):
                    messagebox.showinfo("Info", "Instruksi resep berhasil diperbarui")
                else:
                    messagebox.showerror("Error", "Indeks resep tidak valid")
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Masukkan bilangan bulat untuk indeks")

        btn_perbarui = tk.Button(top, text="Perbarui", command=update_instruksi, bg="light blue")
        btn_perbarui.pack(pady=5)

    def perbarui_resep(self):
        top = tk.Toplevel(self.root)
        top.title("Perbarui Resep")

        tk.Label(top, text="Indeks Resep:").pack(pady=5)
        entry_indeks = tk.Entry(top)
        entry_indeks.pack(pady=5)

        tk.Label(top, text="Nama Baru:").pack(pady=5)
        entry_nama_baru = tk.Entry(top)
        entry_nama_baru.pack(pady=5)

        tk.Label(top, text="Bahan Baru:").pack(pady=5)
        entry_bahan_baru = tk.Text(top, height=3, wrap=tk.WORD)
        entry_bahan_baru.pack(pady=5)

        tk.Label(top, text="Instruksi Baru:").pack(pady=5)
        entry_instruksi_baru = tk.Text(top, height=5, width=50)
        entry_instruksi_baru.pack(pady=5)

        def update_resep():
            try:
                indeks = int(entry_indeks.get())
                nama_baru = entry_nama_baru.get()
                bahan_baru = entry_bahan_baru.get("1.0", tk.END).strip()
                instruksi_baru = entry_instruksi_baru.get("1.0", tk.END).strip()
                resep_baru = Resep(nama_baru, bahan_baru, instruksi_baru)
                if self.manajemen_resep.perbarui_resep(indeks, resep_baru):
                    messagebox.showinfo("Info", "Resep berhasil diperbarui")
                else:
                    messagebox.showerror("Error", "Indeks resep tidak valid")
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Masukkan bilangan bulat untuk indeks")

        btn_perbarui = tk.Button(top, text="Perbarui", command=update_resep, bg="light blue")
        btn_perbarui.pack(pady=5)

    def hapus_resep(self):
        top = tk.Toplevel(self.root)
        top.title("Hapus Resep")

        tk.Label(top, text="Indeks Resep:").pack(pady=5)
        entry_indeks = tk.Entry(top)
        entry_indeks.pack(pady=5)

        def delete_resep():
            try:
                indeks = int(entry_indeks.get())
                if self.manajemen_resep.hapus_resep(indeks):
                    messagebox.showinfo("Info", "Resep berhasil dihapus")
                else:
                    messagebox.showerror("Error", "Indeks resep tidak valid")
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Masukkan bilangan bulat untuk indeks")

        btn_hapus = tk.Button(top, text="Hapus", command=delete_resep, bg="light blue")
        btn_hapus.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ManajemenResepApp(root)
    root.mainloop()
