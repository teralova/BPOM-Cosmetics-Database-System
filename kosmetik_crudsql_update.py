import sqlite3

# 1. Koneksi ke Database
def buat_koneksi():
    conn = sqlite3.connect("kosmetik_berbahaya.db")
    return conn

# 2. Membuat Tabel (Selaras dengan kolom pada tabel web BPOM)
def buat_tabel():
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kosmetik_berbahaya (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_produk TEXT NOT NULL,
            no_izin_edar TEXT,
            kandungan_berbahaya TEXT NOT NULL,
            produsen TEXT,
            no_surat_warning TEXT
        )
    """)
    conn.commit()
    conn.close()

# 3. CREATE: Menambahkan Data Kosmetik Berbahaya (Parameterized Query - Anti SQL Injection)
def tambah_data(nama_produk, no_izin_edar, kandungan_berbahaya, produsen, no_surat_warning):
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kosmetik_berbahaya (nama_produk, no_izin_edar, kandungan_berbahaya, produsen, no_surat_warning) 
        VALUES (?, ?, ?, ?, ?)
    """, (nama_produk, no_izin_edar, kandungan_berbahaya, produsen, no_surat_warning))
    conn.commit()
    conn.close()
    print(f"\n[SUKSES] Data produk '{nama_produk}' berhasil ditambahkan!")

# 4. READ: Menampilkan Semua Data
def tampilkan_data():
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kosmetik_berbahaya")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("\n[INFO] Data kosmetik berbahaya masih kosong.")
    else:
        print("\n=== DAFTAR KOSMETIK MENGANDUNG BAHAN BERBAHAYA (BPOM) ===")
        print(f"{'ID':<4} | {'Nama Produk':<30} | {'No Izin Edar':<15} | {'Bahan Berbahaya':<25} | {'Produsen':<20} | {'No Surat Public Warning':<20}")
        print("-" * 135)
        for row in data:
            # Perbaikan Indeks Array:
            # row[0]: id, row[1]: nama_produk, row[2]: no_izin_edar, 
            # row[3]: kandungan_berbahaya, row[4]: produsen, row[5]: no_surat_warning
            id_prod = str(row[0])
            nama = row[1][:30] if row[1] else "-"
            izin = row[2][:15] if row[2] else "-"
            kandungan = row[3][:25] if row[3] else "-"
            produsen = row[4][:20] if row[4] else "-"
            surat = row[5][:20] if row[5] else "-"
            
            print(f"{id_prod:<4} | {nama:<30} | {izin:<15} | {kandungan:<25} | {produsen:<20} | {surat:<20}")

# 5. UPDATE: Mengubah Data Berdasarkan ID
def update_data(id_produk, kandungan_baru, no_surat_baru):
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE kosmetik_berbahaya 
        SET kandungan_berbahaya = ?, no_surat_warning = ? 
        WHERE id = ?
    """, (kandungan_baru, no_surat_baru, id_produk))
    
    # Cek apakah ada baris yang terpengaruh (ter-update)
    if cursor.rowcount > 0:
        print(f"\n[SUKSES] Data dengan ID {id_produk} berhasil diperbarui!")
    else:
        print(f"\n[WARNING] Data dengan ID {id_produk} tidak ditemukan.")
        
    conn.commit()
    conn.close()

# 6. DELETE: Menghapus Data Berdasarkan ID
def hapus_data(id_produk):
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kosmetik_berbahaya WHERE id = ?", (id_produk,))
    
    # Cek apakah ada baris yang terhapus
    if cursor.rowcount > 0:
        print(f"\n[SUKSES] Data dengan ID {id_produk} berhasil dihapus!")
    else:
        print(f"\n[WARNING] Data dengan ID {id_produk} tidak ditemukan.")
        
    conn.commit()
    conn.close()

# 7. Menu Utama Program
def main():
    buat_tabel()
    while True:
        print("\n=== MENU DATABASE KOSMETIK BERBAHAYA ===")
        print("1. Tambah Data Baru (Create)")
        print("2. Tampilkan Semua Data (Read)")
        print("3. Update Kandungan & No Surat (Update)")
        print("4. Hapus Data (Delete)")
        print("5. Keluar")
        
        pilihan = input("Pilih menu (1-5): ")
        
        if pilihan == "1":
            nama = input("Nama Produk: ")
            no_izin = input("Nomor Izin Edar / Notifikasi (isi '-' jika tidak ada): ")
            kandungan = input("Kandungan Bahan Berbahaya/Dilarang: ")
            produsen = input("Produsen / Pendaftar: ")
            no_surat = input("Nomor Surat Public Warning: ")
            
            # Pemanggilan fungsi dimasukkan ke dalam blok if
            tambah_data(nama, no_izin, kandungan, produsen, no_surat)
                
        elif pilihan == "2":
            tampilkan_data()
            
        elif pilihan == "3":
            tampilkan_data()
            try:
                id_target = int(input("\nMasukkan ID Produk yang akan diupdate: "))
                kandungan_baru = input("Kandungan bahan berbahaya baru: ")
                no_surat_baru = input("Nomor surat public warning baru: ")
                update_data(id_target, kandungan_baru, no_surat_baru)
            except ValueError:
                print("[ERROR] ID harus berupa angka!")
                
        elif pilihan == "4":
            tampilkan_data()
            try:
                id_target = int(input("\nMasukkan ID Produk yang akan dihapus: "))
                hapus_data(id_target)
            except ValueError:
                print("[ERROR] ID harus berupa angka!")
                
        elif pilihan == "5":
            print("\nProgram selesai. Terima kasih!")
            break
        else:
            print("[ERROR] Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()