
#Sifa_007
import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_View import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(
            f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}"
        )

        # Binding tombol simpan
        self.view.btn_simpan.configure(command=self.simpan_data)

        # TAMBAHAN: Binding tombol Update dan Hapus
        self.view.btn_update.configure(command=self.update_data)
        self.view.btn_hapus.configure(command=self.hapus_data)

        # TAMBAHAN: Binding tombol Logout
        self.view.btn_logout.configure(command=self.logout)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan tombol
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled",text="Akses Terkunci (khusus Admin)")

            # TAMBAHAN: Nonaktifkan Update dan Hapus
            self.view.btn_update.configure(state="disabled",text="Akses Terkunci (khusus Admin)")
            self.view.btn_hapus.configure(state="disabled",text="Akses Terkunci (khusus Admin)")

            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.tabel.insert(
                "",
                "end",
                values=(
                    buku['id_buku'],
                    buku['judul'],
                    buku['penulis'],
                    buku['tahun_terbit']
                )
            )

    def simpan_data(self):
        # Proteksi ganda di level Controller
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk menambah data"
            )
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom form harus diisi"
            )
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil disimpan."
            )

            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')

            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    # TAMBAHAN: Fungsi Update
    def update_data(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk memperbarui data"
            )
            return

        selected = self.view.tabel.selection()

        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku yang ingin diperbarui!"
            )
            return

        item = self.view.tabel.item(selected[0])
        id_buku = item["values"][0]

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom harus diisi!"
            )
            return

        berhasil = self.model.update_buku(
            id_buku, judul, penulis, tahun
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Data buku berhasil diperbarui!"
            )
            self.muat_data_tabel()
        else:
            messagebox.showerror(
                "Error",
                "Gagal memperbarui data buku."
            )

    # TAMBAHAN: Fungsi Hapus
    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki izin untuk menghapus data"
            )
            return

        selected = self.view.tabel.selection()

        if not selected:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data buku yang ingin dihapus!"
            )
            return

        item = self.view.tabel.item(selected[0])
        id_buku = item["values"][0]

        konfirmasi = messagebox.askyesno(
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus data buku ini?"
        )

        if konfirmasi:
            berhasil = self.model.delete_buku(id_buku)

            if berhasil:
                messagebox.showinfo(
                    "Sukses",
                    "Data buku berhasil dihapus!"
                )
                self.muat_data_tabel()
            else:
                messagebox.showerror(
                    "Error",
                    "Gagal menghapus data buku."
                )

    # TAMBAHAN: Fungsi Logout
    def logout(self):
        konfirmasi = messagebox.askyesno(
            "Konfirmasi Logout",
            "Apakah Anda yakin ingin logout?"
        )

        if konfirmasi:
            self.view.destroy()

            from controllers.auth_controller import AuthController
            auth = AuthController()
            auth.run()

    def run(self):
        self.view.mainloop()
