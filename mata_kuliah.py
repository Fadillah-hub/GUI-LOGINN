import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ================= KONEKSI DATABASE =================
def koneksi_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="siakad"
    )


# ================= FUNGSI CRUD =================
def ambil_data_dosen():
    try:
        conn = koneksi_database()
        cursor = conn.cursor()
        cursor.execute("SELECT nip FROM dosen ORDER BY nip")
        data = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
        return []


def tampilkan_data():
    for item in tabel.get_children():
        tabel.delete(item)

    try:
        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mk.kode_mk, mk.nama_mk, mk.sks,
                   mk.semester, mk.nip_dosen, d.nama_dosen
            FROM mata_kuliah mk
            LEFT JOIN dosen d ON mk.nip_dosen = d.nip
            ORDER BY mk.kode_mk
        """)

        for row in cursor.fetchall():
            tabel.insert("", tk.END, values=row)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


def bersihkan_form():
    entry_kode.delete(0, tk.END)
    entry_nama.delete(0, tk.END)
    entry_sks.delete(0, tk.END)
    entry_semester.delete(0, tk.END)
    combo_dosen.set("")


def tambah_data():
    kode = entry_kode.get().strip()
    nama = entry_nama.get().strip()
    sks = entry_sks.get().strip()
    semester = entry_semester.get().strip()
    nip = combo_dosen.get().strip()

    if not kode or not nama or not sks or not semester:
        messagebox.showwarning(
            "Peringatan", "Kode, nama, SKS, dan semester wajib diisi."
        )
        return

    try:
        sks = int(sks)
        semester = int(semester)

        if sks <= 0 or not 1 <= semester <= 14:
            messagebox.showwarning(
                "Peringatan", "SKS harus lebih dari 0 dan semester 1-14."
            )
            return

        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO mata_kuliah
            (kode_mk, nama_mk, sks, semester, nip_dosen)
            VALUES (%s, %s, %s, %s, %s)
        """, (kode, nama, sks, semester, nip if nip else None))

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sukses", "Data mata kuliah berhasil ditambahkan.")
        bersihkan_form()
        tampilkan_data()

    except ValueError:
        messagebox.showerror(
            "Input Salah", "SKS dan semester harus berupa angka."
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


def pilih_data(event):
    pilihan = tabel.selection()

    if not pilihan:
        return

    data = tabel.item(pilihan[0], "values")

    bersihkan_form()
    entry_kode.insert(0, data[0])
    entry_nama.insert(0, data[1])
    entry_sks.insert(0, data[2])
    entry_semester.insert(0, data[3])
    combo_dosen.set(data[4] if data[4] else "")

    # Kode mata kuliah menjadi kunci data yang dipilih.
    entry_kode.config(state="disabled")


def edit_data():
    kode = entry_kode.get().strip()
    nama = entry_nama.get().strip()
    sks = entry_sks.get().strip()
    semester = entry_semester.get().strip()
    nip = combo_dosen.get().strip()

    if not kode:
        messagebox.showwarning(
            "Peringatan", "Pilih data mata kuliah dari tabel terlebih dahulu."
        )
        return

    if not nama or not sks or not semester:
        messagebox.showwarning(
            "Peringatan", "Nama, SKS, dan semester wajib diisi."
        )
        return

    try:
        sks = int(sks)
        semester = int(semester)

        if sks <= 0 or not 1 <= semester <= 14:
            messagebox.showwarning(
                "Peringatan", "SKS harus lebih dari 0 dan semester 1-14."
            )
            return

        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE mata_kuliah
            SET nama_mk = %s,
                sks = %s,
                semester = %s,
                nip_dosen = %s
            WHERE kode_mk = %s
        """, (nama, sks, semester, nip if nip else None, kode))

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sukses", "Data mata kuliah berhasil diperbarui.")
        entry_kode.config(state="normal")
        bersihkan_form()
        tampilkan_data()

    except ValueError:
        messagebox.showerror(
            "Input Salah", "SKS dan semester harus berupa angka."
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))


def hapus_data():
    kode = entry_kode.get().strip()

    if not kode:
        messagebox.showwarning(
            "Peringatan", "Pilih data mata kuliah yang ingin dihapus."
        )
        return

    konfirmasi = messagebox.askyesno(
        "Konfirmasi",
        f"Yakin ingin menghapus mata kuliah {kode}?"
    )

    if not konfirmasi:
        return

    try:
        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM mata_kuliah WHERE kode_mk = %s",
            (kode,)
        )

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sukses", "Data mata kuliah berhasil dihapus.")
        entry_kode.config(state="normal")
        bersihkan_form()
        tampilkan_data()

    except mysql.connector.Error as err:
        messagebox.showerror(
            "Gagal Menghapus",
            "Data mungkin sedang digunakan oleh tabel lain.\n\n" + str(err)
        )


# ================= TAMPILAN GUI =================
root = tk.Tk()
root.title("Sistem Informasi Akademik - Data Mata Kuliah")
root.geometry("1050x600")
root.configure(bg="#f0f2f5")

judul = tk.Label(
    root,
    text="DATA MATA KULIAH",
    font=("Arial", 18, "bold"),
    bg="#f0f2f5",
    fg="#1f3a5f"
)
judul.pack(pady=15)

frame_form = tk.LabelFrame(
    root,
    text="Form Mata Kuliah",
    font=("Arial", 10, "bold"),
    bg="#f0f2f5",
    padx=15,
    pady=10
)
frame_form.pack(fill="x", padx=20, pady=5)

tk.Label(frame_form, text="Kode Mata Kuliah", bg="#f0f2f5").grid(
    row=0, column=0, sticky="w", pady=5
)
entry_kode = tk.Entry(frame_form, width=30)
entry_kode.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Nama Mata Kuliah", bg="#f0f2f5").grid(
    row=1, column=0, sticky="w", pady=5
)
entry_nama = tk.Entry(frame_form, width=30)
entry_nama.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Jumlah SKS", bg="#f0f2f5").grid(
    row=0, column=2, sticky="w", pady=5
)
entry_sks = tk.Entry(frame_form, width=30)
entry_sks.grid(row=0, column=3, padx=10, pady=5)

tk.Label(frame_form, text="Semester", bg="#f0f2f5").grid(
    row=1, column=2, sticky="w", pady=5
)
entry_semester = tk.Entry(frame_form, width=30)
entry_semester.grid(row=1, column=3, padx=10, pady=5)

tk.Label(frame_form, text="NIP Dosen", bg="#f0f2f5").grid(
    row=2, column=0, sticky="w", pady=5
)
combo_dosen = ttk.Combobox(
    frame_form,
    width=27,
    values=ambil_data_dosen(),
    state="readonly"
)
combo_dosen.grid(row=2, column=1, padx=10, pady=5)

frame_tombol = tk.Frame(root, bg="#f0f2f5")
frame_tombol.pack(pady=10)

tk.Button(
    frame_tombol, text="Tambah", width=13,
    bg="#198754", fg="white", command=tambah_data
).grid(row=0, column=0, padx=5)

tk.Button(
    frame_tombol, text="Edit", width=13,
    bg="#0d6efd", fg="white", command=edit_data
).grid(row=0, column=1, padx=5)

tk.Button(
    frame_tombol, text="Hapus", width=13,
    bg="#dc3545", fg="white", command=hapus_data
).grid(row=0, column=2, padx=5)

tk.Button(
    frame_tombol, text="Bersihkan", width=13,
    command=lambda: (
        entry_kode.config(state="normal"),
        bersihkan_form()
    )
).grid(row=0, column=3, padx=5)

tk.Button(
    frame_tombol, text="Refresh", width=13,
    command=lambda: (
        combo_dosen.config(values=ambil_data_dosen()),
        tampilkan_data()
    )
).grid(row=0, column=4, padx=5)

frame_tabel = tk.Frame(root)
frame_tabel.pack(fill="both", expand=True, padx=20, pady=10)

kolom = (
    "kode_mk", "nama_mk", "sks",
    "semester", "nip_dosen", "nama_dosen"
)

tabel = ttk.Treeview(
    frame_tabel,
    columns=kolom,
    show="headings"
)

tabel.heading("kode_mk", text="Kode MK")
tabel.heading("nama_mk", text="Nama Mata Kuliah")
tabel.heading("sks", text="SKS")
tabel.heading("semester", text="Semester")
tabel.heading("nip_dosen", text="NIP Dosen")
tabel.heading("nama_dosen", text="Nama Dosen")

tabel.column("kode_mk", width=100, anchor="center")
tabel.column("nama_mk", width=250)
tabel.column("sks", width=60, anchor="center")
tabel.column("semester", width=90, anchor="center")
tabel.column("nip_dosen", width=110, anchor="center")
tabel.column("nama_dosen", width=200)

scrollbar = ttk.Scrollbar(
    frame_tabel, orient="vertical", command=tabel.yview
)
tabel.configure(yscrollcommand=scrollbar.set)

tabel.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tabel.bind("<<TreeviewSelect>>", pilih_data)

tampilkan_data()
root.mainloop()