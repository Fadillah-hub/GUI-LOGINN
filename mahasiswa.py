
# Mengimpor modul tkinter untuk membuat GUI
import tkinter as tk
from tkinter import ttk, messagebox

# Mengimpor mysql.connector untuk koneksi database MySQL
import mysql.connector


# --- KONEKSI DATABASE ---
# Fungsi untuk menghubungkan aplikasi ke database siakad
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="siakad"
    )


# --- FUNGSI CRUD ---

# Fungsi untuk memuat dan menampilkan data mahasiswa
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM mahasiswa")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Gagal mengambil data: {e}"
        )


# Fungsi untuk menambahkan data mahasiswa
def tambah_data():
    nim = entry_nim.get().strip()
    nama = entry_nama.get().strip()
    jk = combo_jk.get()
    tanggal = entry_tanggal.get().strip()
    tempat = entry_tempat.get().strip()
    alamat = entry_alamat.get().strip()
    tlp = entry_tlp.get().strip()
    email = entry_email.get().strip()
    jurusan = entry_jurusan.get().strip()
    angkatan = entry_angkatan.get().strip()
    status = combo_status.get()

    if not nim or not nama or not jk or not tanggal:
        messagebox.showwarning(
            "Peringatan",
            "NIM, Nama, Jenis Kelamin, dan Tanggal Lahir wajib diisi!"
        )
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            INSERT INTO mahasiswa
            (nim, nama_lengkap, jenis_kelamin, tanggal_lahir,
             tempat_lahir, alamat, no_telepon, email, jurusan,
             angkatan, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        val = (
            nim, nama, jk, tanggal,
            tempat or None, alamat or None, tlp or None,
            email or None, jurusan or None,
            int(angkatan) if angkatan else None,
            status or "Aktif"
        )

        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo(
            "Sukses",
            "Data mahasiswa berhasil ditambahkan!"
        )

        clear_fields()
        load_data()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Gagal menambah data: {e}"
        )


# Fungsi untuk mengedit data mahasiswa yang dipilih
def edit_data():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data mahasiswa yang ingin diubah!"
        )
        return

    nim_lama = tree.item(selected[0], "values")[0]

    nim = entry_nim.get().strip()
    nama = entry_nama.get().strip()
    jk = combo_jk.get()
    tanggal = entry_tanggal.get().strip()
    tempat = entry_tempat.get().strip()
    alamat = entry_alamat.get().strip()
    tlp = entry_tlp.get().strip()
    email = entry_email.get().strip()
    jurusan = entry_jurusan.get().strip()
    angkatan = entry_angkatan.get().strip()
    status = combo_status.get()

    if not nim or not nama or not jk or not tanggal:
        messagebox.showwarning(
            "Peringatan",
            "NIM, Nama, Jenis Kelamin, dan Tanggal Lahir wajib diisi!"
        )
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            UPDATE mahasiswa
            SET nim=%s, nama_lengkap=%s, jenis_kelamin=%s,
                tanggal_lahir=%s, tempat_lahir=%s, alamat=%s,
                no_telepon=%s, email=%s, jurusan=%s,
                angkatan=%s, status=%s
            WHERE nim=%s
        """

        val = (
            nim, nama, jk, tanggal,
            tempat or None, alamat or None, tlp or None,
            email or None, jurusan or None,
            int(angkatan) if angkatan else None,
            status or "Aktif", nim_lama
        )

        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo(
            "Sukses",
            "Data mahasiswa berhasil diperbarui!"
        )

        clear_fields()
        load_data()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Gagal memperbarui data: {e}"
        )


# Fungsi untuk menghapus data mahasiswa
def hapus_data():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data mahasiswa yang ingin dihapus!"
        )
        return

    nim = tree.item(selected[0], "values")[0]

    confirm = messagebox.askyesno(
        "Konfirmasi",
        f"Yakin ingin menghapus mahasiswa dengan NIM {nim}?"
    )

    if confirm:
        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM mahasiswa WHERE nim = %s",
                (nim,)
            )

            db.commit()
            cursor.close()
            db.close()

            messagebox.showinfo(
                "Sukses",
                "Data mahasiswa berhasil dihapus!"
            )

            clear_fields()
            load_data()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Gagal menghapus data: {e}"
            )


# Fungsi untuk memilih data dari tabel
def select_item(event=None):
    selected = tree.selection()

    if selected:
        values = tree.item(selected[0], "values")

        clear_fields()

        entry_nim.insert(0, values[0])
        entry_nama.insert(0, values[1])
        combo_jk.set(values[2])
        entry_tanggal.insert(0, str(values[3]))
        entry_tempat.insert(0, values[4] or "")
        entry_alamat.insert(0, values[5] or "")
        entry_tlp.insert(0, values[6] or "")
        entry_email.insert(0, values[7] or "")
        entry_jurusan.insert(0, values[8] or "")
        entry_angkatan.insert(0, values[9] or "")
        combo_status.set(values[10] or "Aktif")


# Fungsi untuk mengosongkan seluruh input
def clear_fields():
    entry_nim.delete(0, tk.END)
    entry_nama.delete(0, tk.END)
    combo_jk.set("")
    entry_tanggal.delete(0, tk.END)
    entry_tempat.delete(0, tk.END)
    entry_alamat.delete(0, tk.END)
    entry_tlp.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_jurusan.delete(0, tk.END)
    entry_angkatan.delete(0, tk.END)
    combo_status.set("Aktif")


# --- GUI MAIN WINDOW ---

root = tk.Tk()
root.title("Aplikasi Data Mahasiswa - SIAKAD")
root.geometry("1250x700")

# Frame form input
frame_form = tk.LabelFrame(
    root,
    text=" Form Data Mahasiswa ",
    padx=10,
    pady=10
)
frame_form.pack(fill="x", padx=15, pady=10)

# Label dan input NIM
tk.Label(frame_form, text="NIM").grid(
    row=0, column=0, sticky="w", padx=5, pady=3
)
entry_nim = tk.Entry(frame_form)
entry_nim.grid(
    row=0, column=1, sticky="ew", padx=5, pady=3
)

# Nama lengkap
tk.Label(frame_form, text="Nama Lengkap").grid(
    row=0, column=2, sticky="w", padx=5, pady=3
)
entry_nama = tk.Entry(frame_form)
entry_nama.grid(
    row=0, column=3, sticky="ew", padx=5, pady=3
)

# Jenis kelamin
tk.Label(frame_form, text="Jenis Kelamin").grid(
    row=1, column=0, sticky="w", padx=5, pady=3
)
combo_jk = ttk.Combobox(
    frame_form,
    values=["Laki-laki", "Perempuan"],
    state="readonly"
)
combo_jk.grid(
    row=1, column=1, sticky="ew", padx=5, pady=3
)

# Tanggal lahir
tk.Label(frame_form, text="Tanggal Lahir (YYYY-MM-DD)").grid(
    row=1, column=2, sticky="w", padx=5, pady=3
)
entry_tanggal = tk.Entry(frame_form)
entry_tanggal.grid(
    row=1, column=3, sticky="ew", padx=5, pady=3
)

# Tempat lahir
tk.Label(frame_form, text="Tempat Lahir").grid(
    row=2, column=0, sticky="w", padx=5, pady=3
)
entry_tempat = tk.Entry(frame_form)
entry_tempat.grid(
    row=2, column=1, sticky="ew", padx=5, pady=3
)

# Alamat
tk.Label(frame_form, text="Alamat").grid(
    row=2, column=2, sticky="w", padx=5, pady=3
)
entry_alamat = tk.Entry(frame_form)
entry_alamat.grid(
    row=2, column=3, sticky="ew", padx=5, pady=3
)

# Nomor telepon
tk.Label(frame_form, text="No Telepon").grid(
    row=3, column=0, sticky="w", padx=5, pady=3
)
entry_tlp = tk.Entry(frame_form)
entry_tlp.grid(
    row=3, column=1, sticky="ew", padx=5, pady=3
)

# Email
tk.Label(frame_form, text="Email").grid(
    row=3, column=2, sticky="w", padx=5, pady=3
)
entry_email = tk.Entry(frame_form)
entry_email.grid(
    row=3, column=3, sticky="ew", padx=5, pady=3
)

# Jurusan
tk.Label(frame_form, text="Jurusan").grid(
    row=4, column=0, sticky="w", padx=5, pady=3
)
entry_jurusan = tk.Entry(frame_form)
entry_jurusan.grid(
    row=4, column=1, sticky="ew", padx=5, pady=3
)

# Angkatan
tk.Label(frame_form, text="Angkatan").grid(
    row=4, column=2, sticky="w", padx=5, pady=3
)
entry_angkatan = tk.Entry(frame_form)
entry_angkatan.grid(
    row=4, column=3, sticky="ew", padx=5, pady=3
)

# Status mahasiswa
tk.Label(frame_form, text="Status").grid(
    row=5, column=0, sticky="w", padx=5, pady=3
)
combo_status = ttk.Combobox(
    frame_form,
    values=["Aktif", "Cuti", "Lulus", "Drop Out"],
    state="readonly"
)
combo_status.set("Aktif")
combo_status.grid(
    row=5, column=1, sticky="ew", padx=5, pady=3
)

frame_form.grid_columnconfigure(1, weight=1)
frame_form.grid_columnconfigure(3, weight=1)

# Tombol CRUD
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=15, pady=5)

tk.Button(
    frame_btn, text="Tambah", bg="#4CAF50", fg="white",
    command=tambah_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Edit", bg="#2196F3", fg="white",
    command=edit_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Hapus", bg="#f44336", fg="white",
    command=hapus_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Clear", bg="#9E9E9E", fg="white",
    command=clear_fields, width=12
).pack(side="left", padx=5)

# Frame tabel
frame_table = tk.Frame(root)
frame_table.pack(
    fill="both", expand=True, padx=15, pady=10
)

columns = (
    "nim", "nama_lengkap", "jenis_kelamin", "tanggal_lahir",
    "tempat_lahir", "alamat", "no_telepon", "email",
    "jurusan", "angkatan", "status"
)

# Scrollbar horizontal dan vertikal
scrollbar_y = ttk.Scrollbar(
    frame_table, orient="vertical"
)
scrollbar_x = ttk.Scrollbar(
    frame_table, orient="horizontal"
)

tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar_y.set,
    xscrollcommand=scrollbar_x.set
)

scrollbar_y.config(command=tree.yview)
scrollbar_x.config(command=tree.xview)

# Header dan lebar kolom tabel
headers = {
    "nim": ("NIM", 90),
    "nama_lengkap": ("Nama Lengkap", 160),
    "jenis_kelamin": ("Jenis Kelamin", 110),
    "tanggal_lahir": ("Tanggal Lahir", 110),
    "tempat_lahir": ("Tempat Lahir", 110),
    "alamat": ("Alamat", 180),
    "no_telepon": ("No Telepon", 120),
    "email": ("Email", 160),
    "jurusan": ("Jurusan", 160),
    "angkatan": ("Angkatan", 80),
    "status": ("Status", 90)
}

for col, (judul, lebar) in headers.items():
    tree.heading(col, text=judul)
    tree.column(col, width=lebar, anchor="w")

tree.grid(row=0, column=0, sticky="nsew")
scrollbar_y.grid(row=0, column=1, sticky="ns")
scrollbar_x.grid(row=1, column=0, sticky="ew")

frame_table.grid_rowconfigure(0, weight=1)
frame_table.grid_columnconfigure(0, weight=1)

# Menghubungkan klik baris dengan form input
tree.bind("<<TreeviewSelect>>", select_item)

# Memuat data saat aplikasi dibuka
load_data()

# Menjalankan GUI
root.mainloop()
