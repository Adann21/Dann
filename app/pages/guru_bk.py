import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.auth import get_current_user, get_current_role

def show_guru_bk():
    user = get_current_user()
    role = get_current_role()
    
    st.title("🧠 Dashboard Guru Bimbingan Konseling")
    st.markdown(f"**Selamat datang, {user.get('full_name', 'Guru BK')}!**")
    
    # Overview statistics
    st.markdown("---")
    st.subheader("📊 Overview Konseling")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Siswa Aktif", "45", "5")
    
    with col2:
        st.metric("Sesi Bulan Ini", "28", "8")
    
    with col3:
        st.metric("Masalah Akademik", "15", "3")
    
    with col4:
        st.metric("Masalah Perilaku", "8", "2")
    
    # Data siswa butuh konseling
    st.markdown("---")
    st.subheader("🎯 Siswa Butuh Perhatian BK")
    
    bk_data = {
        'Nama': ['Andi Wijaya', 'Siti Rahma', 'Budi Santoso', 'Dewi Anggraini', 'Riko Pratama'],
        'Kelas': ['XII TKJ 1', 'XII TKJ 1', 'XII TKJ 1', 'XII TKJ 2', 'XII MM 1'],
        'Jenis Masalah': ['Akademik', 'Perilaku', 'Akademik', 'Sosial', 'Akademik'],
        'Tingkat': ['Sedang', 'Rendah', 'Tinggi', 'Sedang', 'Tinggi'],
        'Status': ['Dalam Proses', 'Baru', 'Prioritas', 'Dalam Proses', 'Prioritas']
    }
    
    bk_df = pd.DataFrame(bk_data)
    st.dataframe(bk_df)
    
    # Grafik masalah konseling
    st.markdown("---")
    st.subheader("📈 Distribusi Masalah Konseling")
    
    masalah_data = {
        'Jenis': ['Akademik', 'Perilaku', 'Sosial', 'Karir', 'Lainnya'],
        'Jumlah': [15, 8, 5, 3, 2]
    }
    
    masalah_df = pd.DataFrame(masalah_data)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(masalah_df['Jumlah'], labels=masalah_df['Jenis'], autopct='%1.1f%%', startangle=90)
    ax.set_title('Distribusi Jenis Masalah Konseling')
    
    st.pyplot(fig)
    
    # Monitoring perkembangan
    st.markdown("---")
    st.subheader("📋 Monitoring Perkembangan")
    
    progress_data = {
        'Nama': ['Andi Wijaya', 'Budi Santoso', 'Dewi Anggraini'],
        'Kelas': ['XII TKJ 1', 'XII TKJ 1', 'XII TKJ 2'],
        'Sesi': ['3/5', '2/6', '4/4'],
        'Perkembangan': ['Positif', 'Stabil', 'Sangat Positif'],
        'Rekomendasi': ['Lanjutkan', 'Intensifkan', 'Selesai']
    }
    
    progress_df = pd.DataFrame(progress_data)
    st.dataframe(progress_df)
    
    # Program intervensi
    st.markdown("---")
    st.subheader("🛠️ Program Intervensi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **Program Berjalan:**
        - Remedial Learning
        - Motivasi Belajar
        - Manajemen Waktu
        - Konseling Karir
        """)
    
    with col2:
        st.warning("""
        **Program Direkomendasikan:**
        - Parenting Workshop
        - Stress Management
        - Career Counseling
        - Group Therapy
        """)
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Jadwal Konseling", use_container_width=True):
            st.info("Fitur jadwal konseling sedang dikembangkan")
    
    with col2:
        if st.button("📝 Catatan Konseling", use_container_width=True):
            st.info("Fitur catatan konseling sedang dikembangkan")
    
    with col3:
        if st.button("📊 Laporan BK", use_container_width=True):
            st.session_state.current_page = "reports"
            st.rerun()

if __name__ == "__main__":
    show_guru_bk()
