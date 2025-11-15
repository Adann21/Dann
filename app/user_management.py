import streamlit as st
import pandas as pd
from datetime import datetime
from app.auth import get_current_user, get_current_role
#from models.database import db

def show_user_management():
    """
    Fungsi untuk menampilkan halaman manajemen pengguna
    Hanya dapat diakses oleh user dengan role admin
    """
    # Ambil data user yang sedang login
    user_login = get_current_user()
    role_login = get_current_role()
    
    # Cek apakah user adalah admin
    if role_login != 'admin':
        st.error("❌ Akses ditolak! Hanya admin yang dapat mengakses halaman ini.")
        return
    
    st.title("👥 Manajemen Pengguna")
    st.markdown("**Halaman Administrator - Kelola User Sistem**")
    
    # Buat tab untuk berbagai fitur manajemen user
    tab_daftar, tab_tambah, tab_edit, tab_hapus = st.tabs([
        "📋 Daftar User", 
        "➕ Tambah User", 
        "✏️ Edit User", 
        "🗑️ Hapus User"
    ])
    
    with tab_daftar:
        st.subheader("Daftar Semua Pengguna")
        # Ambil semua data user dari database PostgreSQL
        data_users = db.get_all_users()
        
        if data_users:
            # Konversi ke DataFrame untuk ditampilkan
            df_users = pd.DataFrame(data_users)
            
            # Sembunyikan kolom password untuk keamanan
            if 'password' in df_users.columns:
                df_tampil = df_users.drop('password', axis=1)
            else:
                df_tampil = df_users
                
            # Tampilkan data dalam tabel
            st.dataframe(df_tampil, use_container_width=True)
            
            # Tampilkan statistik user
            kolom1, kolom2, kolom3, kolom4 = st.columns(4)
            with kolom1:
                st.metric("Total Users", len(data_users))
            with kolom2:
                jumlah_admin = len([u for u in data_users if u.get('role') == 'admin'])
                st.metric("Admin", jumlah_admin)
            with kolom3:
                jumlah_guru = len([u for u in data_users if 'guru' in u.get('role', '')])
                st.metric("Guru", jumlah_guru)
            with kolom4:
                jumlah_wali = len([u for u in data_users if 'wali' in u.get('role', '')])
                st.metric("Wali Kelas", jumlah_wali)
        else:
            st.info("ℹ️ Belum ada user terdaftar dalam sistem")
    
    with tab_tambah:
        st.subheader("Tambah User Baru")
        
        # Form untuk menambah user baru
        with st.form("form_tambah_user"):
            kolom_kiri, kolom_kanan = st.columns(2)
            
            with kolom_kiri:
                input_username = st.text_input("Username*")
                input_password = st.text_input("Password*", type="password")
                input_konfirmasi_password = st.text_input("Konfirmasi Password*", type="password")
            
            with kolom_kanan:
                input_nama_lengkap = st.text_input("Nama Lengkap*")
                input_role = st.selectbox(
                    "Role*",
                    ["admin", "kepala_sekolah", "wali_kelas", "guru_bk", "guru_mapel"]
                )
                
                # Field tambahan berdasarkan role
                if input_role == "guru_mapel":
                    input_mata_pelajaran = st.text_input("Mata Pelajaran")
                elif input_role == "wali_kelas":
                    input_kelas = st.text_input("Kelas (contoh: XII TKJ 1)")
            
            # Tombol submit form
            tombol_submit = st.form_submit_button("💾 Tambah User")
            
            if tombol_submit:
                # Validasi input
                if not all([input_username, input_password, input_konfirmasi_password, input_nama_lengkap]):
                    st.error("❌ Semua field wajib diisi!")
                elif input_password != input_konfirmasi_password:
                    st.error("❌ Password tidak cocok!")
                elif db.get_user(input_username):
                    st.error("❌ Username sudah ada!")
                else:
                    # Buat data user baru
                    user_baru = {
                        "username": input_username,
                        "password": input_password,
                        "role": input_role,
                        "full_name": input_nama_lengkap,
                        "created_at": datetime.now().isoformat(),
                        "created_by": user_login.get('username')
                    }
                    
                    # Tambahkan field khusus role
                    if input_role == "guru_mapel" and input_mata_pelajaran:
                        user_baru["mata_pelajaran"] = input_mata_pelajaran
                    elif input_role == "wali_kelas" and input_kelas:
                        user_baru["kelas"] = input_kelas
                    
                    # Simpan ke database PostgreSQL
                    if db.add_user(user_baru):
                        st.success(f"✅ User {input_username} berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menambah user ke database!")
    
    with tab_edit:
        st.subheader("Edit Data User")
        
        data_users = db.get_all_users()
        if data_users:
            # Daftar username untuk dipilih
            daftar_username = [u['username'] for u in data_users]
            user_terpilih = st.selectbox("Pilih User untuk Edit", daftar_username, key="pilih_edit")
            
            if user_terpilih:
                data_user = db.get_user(user_terpilih)
                if data_user:
                    # Form edit user
                    with st.form("form_edit_user"):
                        kolom_kiri_edit, kolom_kanan_edit = st.columns(2)
                        
                        with kolom_kiri_edit:
                            edit_nama = st.text_input("Nama Lengkap", value=data_user.get('full_name', ''))
                            edit_role = st.selectbox(
                                "Role",
                                ["admin", "kepala_sekolah", "wali_kelas", "guru_bk", "guru_mapel"],
                                index=["admin", "kepala_sekolah", "wali_kelas", "guru_bk", "guru_mapel"].index(
                                    data_user.get('role', 'guru_mapel')
                                ),
                                key="select_role_edit"
                            )
                            
                            # Field khusus role
                            if edit_role == "guru_mapel":
                                edit_mapel = st.text_input("Mata Pelajaran", 
                                                         value=data_user.get('mata_pelajaran', ''))
                            elif edit_role == "wali_kelas":
                                edit_kelas = st.text_input("Kelas", 
                                                         value=data_user.get('kelas', ''))
                        
                        with kolom_kanan_edit:
                            edit_password = st.text_input("Password Baru (kosongkan jika tidak diubah)", 
                                                        type="password", key="input_pass_edit")
                            edit_konfirmasi = st.text_input("Konfirmasi Password", 
                                                          type="password", key="input_confirm_edit")
                        
                        tombol_update = st.form_submit_button("🔄 Update User")
                        
                        if tombol_update:
                            data_update = {
                                "full_name": edit_nama,
                                "role": edit_role,
                                "updated_at": datetime.now().isoformat(),
                                "updated_by": user_login.get('username')
                            }
                            
                            # Update field khusus role
                            if edit_role == "guru_mapel":
                                data_update["mata_pelajaran"] = edit_mapel
                            elif edit_role == "wali_kelas":
                                data_update["kelas"] = edit_kelas
                            
                            # Update password jika diisi
                            if edit_password:
                                if edit_password != edit_konfirmasi:
                                    st.error("❌ Password tidak cocok!")
                                else:
                                    data_update["password"] = edit_password
                            
                            # Proses update ke database PostgreSQL
                            if db.update_user(user_terpilih, data_update):
                                st.success(f"✅ User {user_terpilih} berhasil diupdate!")
                                st.rerun()
                            else:
                                st.error("❌ Gagal update user!")
                else:
                    st.error("❌ User tidak ditemukan!")
        else:
            st.info("ℹ️ Belum ada user untuk di-edit")
    
    with tab_hapus:
        st.subheader("Hapus User dari Sistem")
        
        data_users = db.get_all_users()
        if data_users:
            # Filter user yang bisa dihapus (jangan hapus user admin yang sedang login)
            user_bisa_dihapus = [u for u in data_users if u['username'] != user_login.get('username')]
            
            if user_bisa_dihapus:
                daftar_username_hapus = [u['username'] for u in user_bisa_dihapus]
                detail_users = {u['username']: u for u in user_bisa_dihapus}
                
                user_hapus_terpilih = st.selectbox("Pilih User untuk Dihapus", 
                                                 daftar_username_hapus, key="pilih_hapus")
                
                if user_hapus_terpilih:
                    user_akan_dihapus = detail_users[user_hapus_terpilih]
                    
                    # Peringatan penghapusan
                    st.warning("🚨 PERINGATAN: TINDAKAN INI TIDAK DAPAT DIURAIKAN!")
                    
                    # Tampilkan detail user yang akan dihapus
                    st.write("**Detail User yang akan dihapus:**")
                    kolom_info1, kolom_info2 = st.columns(2)
                    with kolom_info1:
                        st.write(f"**Username:** {user_akan_dihapus['username']}")
                        st.write(f"**Nama:** {user_akan_dihapus.get('full_name', 'N/A')}")
                    with kolom_info2:
                        st.write(f"**Role:** {user_akan_dihapus.get('role', 'N/A')}")
                        st.write(f"**Dibuat:** {user_akan_dihapus.get('created_at', 'N/A')[:10]}")
                    
                    # Konfirmasi tambahan untuk keamanan
                    konfirmasi_hapus = st.text_input(
                        "Ketik 'HAPUS' untuk konfirmasi penghapusan:",
                        placeholder="Ketik HAPUS di sini...",
                        key="input_konfirmasi_hapus"
                    )
                    
                    tombol_hapus = st.button("🗑️ Hapus User Secara Permanen", type="secondary")
                    
                    if tombol_hapus:
                        if konfirmasi_hapus == "HAPUS":
                            # Langsung panggil method PostgreSQL
                            if db.delete_user(user_hapus_terpilih):
                                st.success(f"✅ User {user_hapus_terpilih} berhasil dihapus!")
                                st.rerun()
                            else:
                                st.error("❌ Gagal menghapus user!")
                        else:
                            st.error("❌ Konfirmasi tidak sesuai! Ketik 'HAPUS' untuk melanjutkan.")
            else:
                st.info("ℹ️ Tidak ada user yang dapat dihapus (hanya tersisa user admin saat ini)")
        else:
            st.info("ℹ️ Belum ada user untuk dihapus")

# Jalankan halaman jika file di-execute langsung
if __name__ == "__main__":
    show_user_management()
