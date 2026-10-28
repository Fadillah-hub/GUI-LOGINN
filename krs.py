
# Mengimpor modul tkinter untuk membuat GUI
import tkinter as tk
from tkinter import ttk, messagebox

# Mengimpor mysql.connector untuk koneksi database
import mysql.connector


# --- KONEKSI DATABASE ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="siakad"
    )


# --- FUNGSI CRUD ---

# Fungsi untuk memuat data KRS
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT id_krs, nim, kode_mk, semester_ambil,
                   tahun_ajaran, nilai_huruf, nilai_angka
            FROM krs
            ORDER BY id_krs
        """)

        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Gagal mengambil data KRS: {e}"
        )


# Fungsi untuk menambahkan data KRS
def tambah_data():
    nim = combo_nim.get().strip()
    kode_mk = combo_mk.get().strip()
    semester = entry_semester.get().strip()
    tahun = entry_tahun.get().strip()
    nilai_huruf = combo_nilai_huruf.get().strip()
    nilai_angka = entry_nilai_angka.get().strip()

    if not nim or not kode_mk or not semester or not tahun:
        messagebox.showwarning(
            "Peringatan",
            "NIM, Kode MK, Semester, dan Tahun Ajaran wajib diisi!"
        )
        return

    try:
        semester = int(semester)

        if semester < 1 or semester > 14:
            raise ValueError("Semester harus antara 1 sampai 14.")

        if nilai_angka:
            nilai_angka = float(nilai_angka)
            if not 0 <= nilai_angka <= 4:
                raise ValueError("Nilai angka harus antara 0 sampai 4.")
        else:
            nilai_angka = None

    except ValueError as e:
        messagebox.showwarning("Input Tidak Valid", str(e))
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            INSERT INTO krs
            (nim, kode_mk, semester_ambil, tahun_ajaran,
             nilai_huruf, nilai_angka)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        val = (
            nim, kode_mk, semester, tahun,
            nilai_huruf or None, nilai_angka
        )

        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo(
            "Sukses",
            "Data KRS berhasil ditambahkan!"
        )

        clear_fields()
        load_data()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Gagal menambahkan data KRS: {e}"
        )


# Fungsi untuk mengedit data KRS
def edit_data():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data KRS yang ingin diubah!"
        )
        return

    id_krs = tree.item(selected[0], "values")[0]

    nim = combo_nim.get().strip()
    kode_mk = combo_mk.get().strip()
    semester = entry_semester.get().strip()
    tahun = entry_tahun.get().strip()
    nilai_huruf = combo_nilai_huruf.get().strip()
    nilai_angka = entry_nilai_angka.get().strip()

    if not nim or not kode_mk or not semester or not tahun:
        messagebox.showwarning(
            "Peringatan",
            "NIM, Kode MK, Semester, dan Tahun Ajaran wajib diisi!"
        )
        return

    try:
        semester = int(semester)

        if semester < 1 or semester > 14:
            raise ValueError("Semester harus antara 1 sampai 14.")

        if nilai_angka:
            nilai_angka = float(nilai_angka)
            if not 0 <= nilai_angka <= 4:
                raise ValueError("Nilai angka harus antara 0 sampai 4.")
        else:
            nilai_angka = None

    except ValueError as e:
        messagebox.showwarning("Input Tidak Valid", str(e))
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            UPDATE krs
            SET nim=%s, kode_mk=%s, semester_ambil=%s,
                tahun_ajaran=%s, nilai_huruf=%s, nilai_angka=%s
            WHERE id_krs=%s
        """

        val = (
            nim, kode_mk, semester, tahun,
            nilai_huruf or None, nilai_angka, id_krs
        )

        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo(
            "Sukses",
            "Data KRS berhasil diperbarui!"
        )

        clear_fields()
        load_data()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Gagal memperbarui data KRS: {e}"
        )


# Fungsi untuk menghapus data KRS
def hapus_data():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih data KRS yang ingin dihapus!"
        )
        return

    id_krs = tree.item(selected[0], "values")[0]

    confirm = messagebox.askyesno(
        "Konfirmasi",
        f"Yakin ingin menghapus data KRS ID {id_krs}?"
    )

    if confirm:
        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM krs WHERE id_krs = %s",
                (id_krs,)
            )

            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo(
                "Sukses",
                "Data KRS berhasil dihapus!"
            )

            clear_fields()
            load_data()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Gagal menghapus data KRS: {e}"
            )


# Fungsi untuk memilih data KRS dari tabel
def select_item(event=None):
    selected = tree.selection()

    if selected:
        values = tree.item(selected[0], "values")

        clear_fields()

        combo_nim.set(values[1])
        combo_mk.set(values[2])
        entry_semester.insert(0, values[3])
        entry_tahun.insert(0, values[4])
        combo_nilai_huruf.set(values[5] or "")
        entry_nilai_angka.insert(
            0, "" if values[6] is None else values[6]
        )


# Fungsi untuk mengosongkan form
def clear_fields():
    combo_nim.set("")
    combo_mk.set("")
    entry_semester.delete(0, tk.END)
    entry_tahun.delete(0, tk.END)
    combo_nilai_huruf.set("")
    entry_nilai_angka.delete(0, tk.END)


# --- GUI MAIN WINDOW ---
root = tk.Tk()
root.title("Aplikasi KRS - SIAKAD")
root.geometry("1100x600")


# Frame form KRS
frame_form = tk.LabelFrame(
    root,
    text=" Form Kartu Rencana Studi ",
    padx=10,
    pady=10
)
frame_form.pack(fill="x", padx=15, pady=10)


# NIM mahasiswa
tk.Label(frame_form, text="NIM Mahasiswa").grid(
    row=0, column=0, sticky="w", padx=5, pady=5
)

combo_nim = ttk.Combobox(frame_form, state="readonly")
combo_nim.grid(
    row=0, column=1, sticky="ew", padx=5, pady=5
)


# Kode mata kuliah
tk.Label(frame_form, text="Kode Mata Kuliah").grid(
    row=0, column=2, sticky="w", padx=5, pady=5
)

combo_mk = ttk.Combobox(frame_form, state="readonly")
combo_mk.grid(
    row=0, column=3, sticky="ew", padx=5, pady=5
)


# Semester yang diambil
tk.Label(frame_form, text="Semester Ambil").grid(
    row=1, column=0, sticky="w", padx=5, pady=5
)

entry_semester = tk.Entry(frame_form)
entry_semester.grid(
    row=1, column=1, sticky="ew", padx=5, pady=5
)


# Tahun ajaran
tk.Label(frame_form, text="Tahun Ajaran").grid(
    row=1, column=2, sticky="w", padx=5, pady=5
)

entry_tahun = tk.Entry(frame_form)
entry_tahun.grid(
    row=1, column=3, sticky="ew", padx=5, pady=5
)


# Nilai huruf
tk.Label(frame_form, text="Nilai Huruf").grid(
    row=2, column=0, sticky="w", padx=5, pady=5
)

combo_nilai_huruf = ttk.Combobox(
    frame_form,
    values=["A", "A-", "B+", "B", "B-", "C+", "C", "D", "E"],
    state="readonly"
)
combo_nilai_huruf.grid(
    row=2, column=1, sticky="ew", padx=5, pady=5
)


# Nilai angka
tk.Label(frame_form, text="Nilai Angka (0-4)").grid(
    row=2, column=2, sticky="w", padx=5, pady=5
)

entry_nilai_angka = tk.Entry(frame_form)
entry_nilai_angka.grid(
    row=2, column=3, sticky="ew", padx=5, pady=5
)


frame_form.grid_columnconfigure(1, weight=1)
frame_form.grid_columnconfigure(3, weight=1)


# --- TOMBOL CRUD ---
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=15, pady=5)

tk.Button(
    frame_btn, text="Tambah",
    bg="#4CAF50", fg="white",
    command=tambah_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Edit",
    bg="#2196F3", fg="white",
    command=edit_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Hapus",
    bg="#f44336", fg="white",
    command=hapus_data, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Clear",
    bg="#9E9E9E", fg="white",
    command=clear_fields, width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn, text="Refresh",
    command=load_data, width=12
).pack(side="left", padx=5)


# --- TABEL KRS ---
frame_table = tk.Frame(root)
frame_table.pack(
    fill="both", expand=True, padx=15, pady=10
)

columns = (
    "id_krs", "nim", "kode_mk", "semester_ambil",
    "tahun_ajaran", "nilai_huruf", "nilai_angka"
)

scrollbar_y = ttk.Scrollbar(
    frame_table, orient="vertical"
)

tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar_y.set
)

scrollbar_y.config(command=tree.yview)

tree.heading("id_krs", text="ID KRS")
tree.heading("nim", text="NIM")
tree.heading("kode_mk", text="Kode MK")
tree.heading("semester_ambil", text="Semester")
tree.heading("tahun_ajaran", text="Tahun Ajaran")
tree.heading("nilai_huruf", text="Nilai Huruf")
tree.heading("nilai_angka", text="Nilai Angka")

tree.column("id_krs", width=80, anchor="center")
tree.column("nim", width=120, anchor="center")
tree.column("kode_mk", width=120, anchor="center")
tree.column("semester_ambil", width=100, anchor="center")
tree.column("tahun_ajaran", width=130, anchor="center")
tree.column("nilai_huruf", width=100, anchor="center")
tree.column("nilai_angka", width=100, anchor="center")

tree.pack(side="left", fill="both", expand=True)
scrollbar_y.pack(side="right", fill="y")

tree.bind("<<TreeviewSelect>>", select_item)


# --- MEMUAT DATA DROPDOWN ---
def load_dropdown():
    try:
        db = connect_db()
        cursor = db.cursor()

        # Mengambil NIM dari tabel mahasiswa
        cursor.execute(
            "SELECT nim FROM mahasiswa ORDER BY nim"
        )
        combo_nim["values"] = [
            row[0] for row in cursor.fetchall()
        ]

        # Mengambil kode MK dari tabel mata_kuliah
        cursor.execute(
            "SELECT kode_mk FROM mata_kuliah ORDER BY kode_mk"
        )
        combo_mk["values"] = [
            row[0] for row in cursor.fetchall()
        ]

        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Gagal memuat pilihan mahasiswa/mata kuliah: {e}"
        )


# Memuat data saat aplikasi dibuka
load_dropdown()
load_data()

# Menjalankan GUI
root.mainloop()
