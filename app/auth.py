import streamlit as st
#from models.database import db

def login():
    """
    Fungsi untuk menampilkan halaman login
    Menangani proses autentikasi pengguna
    """
    # Judul halaman login
    st.title("🔐 Login Sistem Prediksi Kelulusan")
    st.subheader("SMKN 1 Sandai")
    
    # Expandable section untuk informasi akun demo
    # expanded=False agar tidak terbuka secara default
    with st.expander("📋 Informasi Login Demo", expanded=False):
        st.info("""
        **Demo Accounts:**
        
        **Administrator**
        - Username: admin | Password: admin123
        
        **Kepala Sekolah**  
        - Username: kepsek | Password: kepsek123
        
        **Guru Mata Pelajaran**
        - Matematika: siti_math | guru123
        - Bahasa Indonesia: budi_bindo | guru123  
        - Bahasa Inggris: dewi_bing | guru123
        - TKJ: riko_tkj | guru123
        - Multimedia: maya_mm | guru123
        - RPL: hendra_rpl | guru123
        
        **Guru BK**
        - Username: linda_bk | Password: bk123
        
        **Wali Kelas**
        - XII TKJ 1: fajar_tkj1 | wali123
        - XII TKJ 2: intan_tkj2 | wali123  
        - XII MM 1: agus_mm1 | wali123
        - XII MM 2: nina_mm2 | wali123
        - XII RPL 1: dodi_rpl1 | wali123
        - XII RPL 2: sari_rpl2 | wali123
        """)
    
    # Form login menggunakan st.form untuk grouping input
    with st.form("login_form"):
        # Input field untuk username
        username_input = st.text_input("Username")
        
        # Input field untuk password dengan type password
        password_input = st.text_input("Password", type="password")
        
        # Submit button untuk login
        login_submit = st.form_submit_button("Login")
        
        # Proses ketika tombol login ditekan
        if login_submit:
            # Validasi input tidak boleh kosong
            if not username_input or not password_input:
                st.error("Username dan password harus diisi!")
                return
                
            # Ambil data user dari database
            user_data = db.get_user(username_input)
            
            # Cek apakah user exist dan password match
            if user_data and user_data.get("password") == password_input:
                # Set session state untuk user yang login
                st.session_state.user = user_data
                st.session_state.logged_in = True
                st.session_state.role = user_data.get("role")
                st.session_state.current_page = "beranda"
                
                # Tampilkan pesan sukses
                st.success(f"Login berhasil! Selamat datang {user_data.get('full_name')}!")
                
                # Rerun aplikasi untuk redirect ke halaman utama
                st.rerun()
            else:
                # Tampilkan error jika kredensial salah
                st.error("Username atau password salah!")

def logout():
    """
    Fungsi untuk logout user
    Menghapus semua data dari session state
    """
    # Tombol logout
    if st.button("Logout"):
        # Hapus semua key dari session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Rerun aplikasi untuk kembali ke halaman login
        st.rerun()

def check_authentication():
    """
    Fungsi untuk mengecek status autentikasi user
    Jika belum login, tampilkan halaman login dan stop eksekusi
    """
    # Cek flag logged_in di session state
    if not st.session_state.get("logged_in"):
        # Tampilkan halaman login
        login()
        # Stop eksekusi code selanjutnya
        st.stop()

def get_current_user():
    """
    Fungsi untuk mendapatkan data user yang sedang login
    Returns:
        dict: Data user dari session state
    """
    return st.session_state.get("user")

def get_current_role():
    """
    Fungsi untuk mendapatkan role user yang sedang login
    Returns:
        str: Role user dari session state
    """
    return st.session_state.get("role")
