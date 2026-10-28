
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ==============================
# KONEKSI DATABASE
# ==============================
def koneksi_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="siakad"
    )


# ==============================
# WINDOW UTAMA
# ==============================
root = tk.Tk()
root.title("SIAKAD - Data Pembayaran UKT")
root.geometry("1100x600")
root.configure(bg="#f0f2f5")


# ==============================
# JUDUL
# ==============================
tk.Label(
    root,
    text="DATA PEMBAYARAN UKT",
    font=("Arial", 20, "bold"),
    bg="#273c75",
    fg="white",
    pady=15
).pack(fill="x")


# ==============================
# FORM INPUT
# ==============================
frame_form = tk.LabelFrame(
    root,
    text="Form Pembayaran UKT",
    font=("Arial", 11, "bold"),
    bg="white",
    padx=15,
    pady=12
)
frame_form.pack(fill="x", padx=20, pady=15)


kolom = [
    ("ID Pembayaran", "id_pembayaran"),
    ("NIM", "nim"),
    ("Jumlah Bayar", "jumlah_bayar"),
    ("Tanggal Bayar", "tanggal_bayar"),
    ("Status", "status")
]

entries = {}

for i, (label, field) in enumerate(kolom):
    tk.Label(
        frame_form,
        text=label,
        font=("Arial", 10),
        bg="white"
    ).grid(row=0, column=i, padx=10, pady=5, sticky="w")

    if field == "status":
        widget = ttk.Combobox(
            frame_form,
            values=["Belum Lunas", "Lunas"],
            state="readonly",
            width=19
        )
    else:
        widget = tk.Entry(frame_form, width=22)

    widget.grid(row=1, column=i, padx=10, pady=5)
    entries[field] = widget


# ==============================
# TABEL DATA
# ==============================
frame_tabel = tk.Frame(root)
frame_tabel.pack(fill="both", expand=True, padx=20, pady=5)

scroll_y = ttk.Scrollbar(frame_tabel, orient="vertical")

tabel = ttk.Treeview(
    frame_tabel,
    columns=[field for label, field in kolom],
    show="headings",
    yscrollcommand=scroll_y.set
)

scroll_y.config(command=tabel.yview)

for label, field in kolom:
    tabel.heading(field, text=label)
    tabel.column(field, width=190, anchor="center")

tabel.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")


# ==============================
# FUNGSI BERSIHKAN FORM
# ==============================
def bersihkan_form():
    for field, widget in entries.items():
        if isinstance(widget, ttk.Combobox):
            widget.set("")
        else:
            widget.delete(0, tk.END)


# ==============================
# TAMPILKAN DATA
# ==============================
def tampilkan_data():
    try:
        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_pembayaran, nim, jumlah_bayar,
                   tanggal_bayar, status
            FROM pembayaran_ukt
        """)

        data = cursor.fetchall()
        tabel.delete(*tabel.get_children())

        for row in data:
            tabel.insert("", tk.END, values=row)

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Error Database", str(e))


# ==============================
# TAMBAH DATA
# ==============================
def tambah_data():
    values = [
        entries[field].get().strip()
        for label, field in kolom
    ]

    if not all(values):
        messagebox.showwarning(
            "Peringatan",
            "Semua kolom wajib diisi!"
        )
        return

    try:
        jumlah = float(values[2])

        if jumlah <= 0:
            messagebox.showwarning(
                "Peringatan",
                "Jumlah pembayaran harus lebih dari 0!"
            )
            return

        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pembayaran_ukt
            (id_pembayaran, nim, jumlah_bayar,
             tanggal_bayar, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            values[0], values[1], jumlah,
            values[3], values[4]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        tampilkan_data()
        bersihkan_form()

        messagebox.showinfo(
            "Sukses",
            "Pembayaran UKT berhasil ditambahkan!"
        )

    except ValueError:
        messagebox.showerror(
            "Input Salah",
            "Jumlah bayar harus berupa angka!"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Error Database", str(e))


# ==============================
# PILIH DATA
# ==============================
def pilih_data(event):
    selected = tabel.selection()

    if not selected:
        return

    data = tabel.item(selected[0], "values")

    for i, (label, field) in enumerate(kolom):
        widget = entries[field]

        if isinstance(widget, ttk.Combobox):
            widget.set(data[i])
        else:
            widget.delete(0, tk.END)
            widget.insert(0, data[i])


# ==============================
# UBAH DATA
# ==============================
def ubah_data():
    values = [
        entries[field].get().strip()
        for label, field in kolom
    ]

    if not all(values):
        messagebox.showwarning(
            "Peringatan",
            "Pilih data dan lengkapi semua kolom!"
        )
        return

    try:
        jumlah = float(values[2])

        if jumlah <= 0:
            messagebox.showwarning(
                "Peringatan",
                "Jumlah pembayaran harus lebih dari 0!"
            )
            return

        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pembayaran_ukt
            SET nim=%s, jumlah_bayar=%s,
                tanggal_bayar=%s, status=%s
            WHERE id_pembayaran=%s
        """, (
            values[1], jumlah, values[3],
            values[4], values[0]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        tampilkan_data()
        bersihkan_form()

        messagebox.showinfo(
            "Sukses",
            "Data pembayaran UKT berhasil diubah!"
        )

    except ValueError:
        messagebox.showerror(
            "Input Salah",
            "Jumlah bayar harus berupa angka!"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Error Database", str(e))


# ==============================
# HAPUS DATA
# ==============================
def hapus_data():
    selected = tabel.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data yang ingin dihapus!"
        )
        return

    id_pembayaran = tabel.item(
        selected[0], "values"
    )[0]

    if not messagebox.askyesno(
        "Konfirmasi",
        f"Hapus pembayaran {id_pembayaran}?"
    ):
        return

    try:
        conn = koneksi_database()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM pembayaran_ukt
            WHERE id_pembayaran=%s
        """, (id_pembayaran,))

        conn.commit()
        cursor.close()
        conn.close()

        tampilkan_data()
        bersihkan_form()

        messagebox.showinfo(
            "Sukses",
            "Data pembayaran UKT berhasil dihapus!"
        )

    except mysql.connector.Error as e:
        messagebox.showerror("Error Database", str(e))


# ==============================
# TOMBOL
# ==============================
frame_tombol = tk.Frame(root, bg="#f0f2f5")
frame_tombol.pack(pady=12)

daftar_tombol = [
    ("Tambah Data", tambah_data, "#44bd32"),
    ("Ubah Data", ubah_data, "#0097e6"),
    ("Hapus Data", hapus_data, "#e84118"),
    ("Bersihkan", bersihkan_form, "#718093"),
    ("Refresh", tampilkan_data, "#8c7ae6")
]

for teks, fungsi, warna in daftar_tombol:
    tk.Button(
        frame_tombol,
        text=teks,
        command=fungsi,
        bg=warna,
        fg="white",
        font=("Arial", 10, "bold"),
        width=14,
        pady=7,
        cursor="hand2"
    ).pack(side="left", padx=5)


tabel.bind("<<TreeviewSelect>>", pilih_data)

tampilkan_data()

root.mainloop()
