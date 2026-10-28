
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

# Fungsi untuk memuat data jadwal kuliah
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT id_jadwal, kode_mk, hari,
                   jam_mulai, jam_selesai, ruangan
            FROM jadwal_kuliah
            ORDER BY id_jadwal
        """)

        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Gagal mengambil data jadwal kuliah: {e}"
        )


# Fungsi untuk menambahkan jadwal kuliah
def tambah_data():
    kode_mk = combo_mk.get().strip()
    hari = combo_hari.get()
    jam_mulai = entry_mulai.get().strip()
    jam_selesai = entry_selesai.get().strip()
    ruangan = entry_ruangan.get().strip()

    if not kode_mk or not hari or not jam_mulai or not jam_selesai:
        messagebox.showwarning(
            "Peringatan",
            "Kode MK, Hari, Jam Mulai, dan Jam Selesai wajib diisi!"
        )
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            INSERT INTO jadwal_kuliah
            (kode_mk, hari, jam_mulai, jam_selesai, ruangan)
            VALUES (%s, %s, %s, %s, %s)
        """

        val = (
            kode_mk,
            hari,
            jam_mulai,
            jam_selesai,
            ruangan or None
        )

        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo(
            "Sukses",
            "Jadwal kuliah berhasil ditambahkan!"
        )

        clear_fields()
        load_data()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Gagal menambahkan jadwal: {e}"
        )


# Fungsi untuk mengedit jadwal kuliah
def edit_data():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih jadwal yang ingin diubah!"
        )
        return

    id_jadwal = tree.item(selected[0], "values")[0]

    kode_mk = combo_mk.get().strip()
    hari = combo_hari.get()
    jam_mulai = entry_mulai.get().strip()
    jam_selesai = entry_selesai.get().strip()
    ruangan = entry_ruangan.get().strip()

    if not kode_mk or not hari or not jam_mulai or not jam_selesai:
        messagebox.showwarning(
            "Peringatan",
            "Kode MK, Hari, Jam Mulai, dan Jam Selesai wajib diisi!"
        )
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
            UPDATE jadwal_kuliah
            SET kode_mk=%s, hari=%s, jam_mulai=%s,
                jam_selesai=%s, ruangan=%s
            WHERE id_jadwal=%s
        """

        val = (
            kode_mk,
            hari,
            jam_mulai,
            jam_selesai,
            ruangan or None,
            id_jadwal
        )

        cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()

        messagebox.showinfo(
            "Sukses",
            "Jadwal kuliah berhasil diperbarui!"
        )

        clear_fields()
        load_data()

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Gagal memperbarui jadwal: {e}"
        )


# Fungsi untuk menghapus jadwal kuliah
def hapus_data():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Peringatan",
            "Pilih jadwal yang ingin dihapus!"
        )
        return

    id_jadwal = tree.item(selected[0], "values")[0]

    confirm = messagebox.askyesno(
        "Konfirmasi",
        f"Yakin ingin menghapus jadwal ID {id_jadwal}?"
    )

    if confirm:
        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM jadwal_kuliah WHERE id_jadwal = %s",
                (id_jadwal,)
            )

            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo(
                "Sukses",
                "Jadwal kuliah berhasil dihapus!"
            )

            clear_fields()
            load_data()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Gagal menghapus jadwal: {e}"
            )


# Fungsi untuk memilih jadwal dari tabel
def select_item(event=None):
    selected = tree.selection()

    if selected:
        values = tree.item(selected[0], "values")

        clear_fields()

        combo_mk.set(values[1])
        combo_hari.set(values[2])
        entry_mulai.insert(0, str(values[3]))
        entry_selesai.insert(0, str(values[4]))
        entry_ruangan.insert(0, values[5] or "")


# Fungsi untuk mengosongkan form
def clear_fields():
    combo_mk.set("")
    combo_hari.set("")
    entry_mulai.delete(0, tk.END)
    entry_selesai.delete(0, tk.END)
    entry_ruangan.delete(0, tk.END)


# --- GUI MAIN WINDOW ---
root = tk.Tk()
root.title("Aplikasi Jadwal Kuliah - SIAKAD")
root.geometry("1000x600")


# Frame form jadwal kuliah
frame_form = tk.LabelFrame(
    root,
    text=" Form Jadwal Kuliah ",
    padx=10,
    pady=10
)
frame_form.pack(fill="x", padx=15, pady=10)


# Kode mata kuliah
tk.Label(frame_form, text="Kode Mata Kuliah").grid(
    row=0, column=0, sticky="w", padx=5, pady=5
)

combo_mk = ttk.Combobox(
    frame_form,
    state="readonly"
)
combo_mk.grid(
    row=0, column=1, sticky="ew", padx=5, pady=5
)


# Hari
tk.Label(frame_form, text="Hari").grid(
    row=0, column=2, sticky="w", padx=5, pady=5
)

combo_hari = ttk.Combobox(
    frame_form,
    values=[
        "Senin", "Selasa", "Rabu",
        "Kamis", "Jumat", "Sabtu"
    ],
    state="readonly"
)
combo_hari.grid(
    row=0, column=3, sticky="ew", padx=5, pady=5
)


# Jam mulai
tk.Label(frame_form, text="Jam Mulai (HH:MM:SS)").grid(
    row=1, column=0, sticky="w", padx=5, pady=5
)

entry_mulai = tk.Entry(frame_form)
entry_mulai.grid(
    row=1, column=1, sticky="ew", padx=5, pady=5
)


# Jam selesai
tk.Label(frame_form, text="Jam Selesai (HH:MM:SS)").grid(
    row=1, column=2, sticky="w", padx=5, pady=5
)

entry_selesai = tk.Entry(frame_form)
entry_selesai.grid(
    row=1, column=3, sticky="ew", padx=5, pady=5
)


# Ruangan
tk.Label(frame_form, text="Ruangan").grid(
    row=2, column=0, sticky="w", padx=5, pady=5
)

entry_ruangan = tk.Entry(frame_form)
entry_ruangan.grid(
    row=2, column=1, sticky="ew", padx=5, pady=5
)


frame_form.grid_columnconfigure(1, weight=1)
frame_form.grid_columnconfigure(3, weight=1)


# --- TOMBOL CRUD ---
frame_btn = tk.Frame(root)
frame_btn.pack(fill="x", padx=15, pady=5)

tk.Button(
    frame_btn,
    text="Tambah",
    bg="#4CAF50",
    fg="white",
    command=tambah_data,
    width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn,
    text="Edit",
    bg="#2196F3",
    fg="white",
    command=edit_data,
    width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn,
    text="Hapus",
    bg="#f44336",
    fg="white",
    command=hapus_data,
    width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn,
    text="Clear",
    bg="#9E9E9E",
    fg="white",
    command=clear_fields,
    width=12
).pack(side="left", padx=5)

tk.Button(
    frame_btn,
    text="Refresh",
    command=load_data,
    width=12
).pack(side="left", padx=5)


# --- TABEL JADWAL KULIAH ---
frame_table = tk.Frame(root)
frame_table.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

columns = (
    "id_jadwal",
    "kode_mk",
    "hari",
    "jam_mulai",
    "jam_selesai",
    "ruangan"
)

scrollbar_y = ttk.Scrollbar(
    frame_table,
    orient="vertical"
)

tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings",
    yscrollcommand=scrollbar_y.set
)

scrollbar_y.config(command=tree.yview)

tree.heading("id_jadwal", text="ID Jadwal")
tree.heading("kode_mk", text="Kode Mata Kuliah")
tree.heading("hari", text="Hari")
tree.heading("jam_mulai", text="Jam Mulai")
tree.heading("jam_selesai", text="Jam Selesai")
tree.heading("ruangan", text="Ruangan")

tree.column("id_jadwal", width=90, anchor="center")
tree.column("kode_mk", width=150, anchor="center")
tree.column("hari", width=120, anchor="center")
tree.column("jam_mulai", width=150, anchor="center")
tree.column("jam_selesai", width=150, anchor="center")
tree.column("ruangan", width=200, anchor="w")

tree.pack(side="left", fill="both", expand=True)
scrollbar_y.pack(side="right", fill="y")

tree.bind("<<TreeviewSelect>>", select_item)


# --- MEMUAT KODE MATA KULIAH DARI DATABASE ---
def load_kode_mk():
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT kode_mk FROM mata_kuliah ORDER BY kode_mk"
        )

        data = [row[0] for row in cursor.fetchall()]
        combo_mk["values"] = data

        cursor.close()
        db.close()

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            f"Gagal mengambil kode mata kuliah: {e}"
        )


# Memuat data saat aplikasi dibuka
load_kode_mk()
load_data()

# Menjalankan aplikasi
root.mainloop()
