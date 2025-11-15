import streamlit as st
from app.auth import get_current_user, get_current_role

def show():
    user = get_current_user()
    role = get_current_role()
    
    st.title("🎓 Selamat Datang di Sistem Prediksi Kelulusan")
    st.subheader(f"SMKN 1 Sandai")
    
    # Welcome message berdasarkan role
    role_messages = {
        "admin": "Anda memiliki akses penuh untuk mengelola sistem, user, dan semua data.",
        "kepala_sekolah": "Anda dapat melihat overview sekolah, strategi, dan laporan prediksi kelulusan.",
        "guru_mapel": "Anda dapat memantau nilai siswa, melakukan prediksi, dan melihat laporan mata pelajaran.",
        "guru_bk": "Anda dapat memantau perkembangan konseling, masalah siswa, dan program intervensi.", 
        "wali_kelas": "Anda dapat memantau kelas, kehadiran, dan koordinasi dengan guru lain."
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Tampilkan info user detail
        st.markdown(f"""
        **Halo, {user.get('full_name', 'User')}!** 👋
        
        **Jabatan:** {user.get('jabatan', role.replace('_', ' ').title())}
        **Role Akses:** {role.replace('_', ' ').title()}
        {'**Mata Pelajaran:** ' + user.get('mata_pelajaran', '') if user.get('mata_pelajaran') else ''}
        {'**Kelas:** ' + user.get('kelas', '') if user.get('kelas') else ''}
        {'**Kelas Diajar:** ' + ', '.join(user.get('kelas_diajar', [])) if user.get('kelas_diajar') else ''}
        
        {role_messages.get(role, 'Selamat menggunakan sistem prediksi kelulusan.')}
        
        ### 🚀 Fitur yang tersedia:
        - 📊 Dashboard analisis data
        - 🔮 Prediksi kelulusan siswa  
        - 📈 Visualisasi data statistik
        - 📋 Laporan hasil prediksi
        {'- 👥 Manajemen pengguna' if role == 'admin' else ''}
        
        ### 📖 Petunjuk Penggunaan:
        1. Gunakan menu navigasi di sidebar
        2. Upload data siswa melalui menu Dashboard
        3. Lihat prediksi di menu Prediction  
        4. Export laporan jika diperlukan
        """)
    
    with col2:
        st.info("""
        **ℹ️ Info Sistem:**
        - Versi: 2.0.0
        - Status: Production Ready
        - Update: Oktober 2024
        - Support: Multi-role Access
        """)
        
        # Quick user info card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-top: 1rem;">
            <h4>👤 Info Login</h4>
            <p><strong>Username:</strong><br>{username}</p>
            <p><strong>Role:</strong><br>{role}</p>
        </div>
        """.format(
            username=user.get('username', 'N/A'),
            role=role.replace('_', ' ').title()
        ), unsafe_allow_html=True)
    
    # Quick stats berdasarkan role
    st.markdown("---")
    st.subheader("📈 Statistik Cepat")
    
    if role == "admin":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total User", "16", "0")
        with col2:
            st.metric("Active Sessions", "1", "0") 
        with col3:
            st.metric("System Status", "Online", "0")
        with col4:
            st.metric("Data Records", "150", "0")
    
    elif role == "kepala_sekolah":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Siswa", "480", "15")
        with col2:
            st.metric("Guru & Staff", "45", "2")
        with col3:
            st.metric("Rata-rata Nilai", "78.2", "1.5")
        with col4:
            st.metric("Kelulusan", "92%", "3%")
    
    elif role == "guru_mapel":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Siswa Diajar", "150", "12")
        with col2:
            st.metric("Rata-rata Nilai", "78.5", "2.1")
        with col3:
            st.metric("Remedial Needed", "8", "2")
        with col4:
            st.metric("Top Students", "25", "3")
    
    elif role == "guru_bk":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Siswa Aktif", "45", "5")
        with col2:
            st.metric("Sesi Bulan Ini", "28", "8")
        with col3:
            st.metric("Masalah Akademik", "15", "3")
        with col4:
            st.metric("Progress Positif", "22", "6")
    
    elif role == "wali_kelas":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Siswa Kelas", "32", "2")
        with col2:
            st.metric("Rata-rata Kelas", "79.2", "1.8")
        with col3:
            st.metric("Kehadiran", "94%", "2%")
        with col4:
            st.metric("Prediksi Lulus", "28", "4")
    
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Siswa", "0", "0")
        with col2:
            st.metric("Prediksi Lulus", "0", "0")
        with col3:
            st.metric("Prediksi Tidak", "0", "0")
        with col4:
            st.metric("Akurasi Model", "0%", "0%")

if __name__ == "__main__":
    show()
