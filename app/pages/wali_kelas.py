import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.auth import get_current_user, get_current_role

def show_wali_kelas():
    user = get_current_user()
    role = get_current_role()
    
    st.title("👥 Dashboard Wali Kelas")
    st.markdown(f"**Selamat datang, {user.get('full_name', 'Wali Kelas')}!**")
    
    # Class overview
    st.markdown("---")
    st.subheader("📊 Overview Kelas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Siswa", "32", "2")
    
    with col2:
        st.metric("Rata-rata Kelas", "79.2", "1.8")
    
    with col3:
        st.metric("Kehadiran", "94%", "2%")
    
    with col4:
        st.metric("Prediksi Lulus", "28", "4")
    
    # Student performance
    st.markdown("---")
    st.subheader("📈 Performa Siswa")
    
    siswa_data = {
        'Nama': ['Andi Wijaya', 'Siti Rahma', 'Budi Santoso', 'Dewi Anggraini', 'Riko Pratama', 'Maya Sari'],
        'Matematika': [85, 78, 65, 88, 72, 60],
        'B. Indonesia': [78, 80, 70, 85, 75, 65],
        'B. Inggris': [82, 76, 68, 90, 70, 62],
        'Kejuruan': [88, 82, 75, 92, 78, 70],
        'Rata-rata': [83.3, 79.0, 69.5, 88.8, 73.8, 64.3],
        'Status': ['Excellent', 'Good', 'Need Help', 'Excellent', 'Good', 'Need Help']
    }
    
    siswa_df = pd.DataFrame(siswa_data)
    st.dataframe(siswa_df)
    
    # Grafik performa
    fig, ax = plt.subplots(figsize=(12, 6))
    
    subjects = ['Matematika', 'B. Indonesia', 'B. Inggris', 'Kejuruan']
    values = [
        siswa_df['Matematika'].mean(),
        siswa_df['B. Indonesia'].mean(),
        siswa_df['B. Inggris'].mean(), 
        siswa_df['Kejuruan'].mean()
    ]
    
    ax.bar(subjects, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax.set_ylabel('Rata-rata Nilai')
    ax.set_title('Rata-rata Nilai per Mata Pelajaran')
    ax.grid(axis='y', alpha=0.3)
    
    st.pyplot(fig)
    
    # Students need attention
    st.markdown("---")
    st.subheader("🎯 Siswa Perlu Perhatian")
    
    perhatian_data = {
        'Nama': ['Budi Santoso', 'Maya Sari', 'Riko Pratama'],
        'Mata Pelajaran': ['Matematika', 'Semua', 'B. Inggris'],
        'Nilai': [65, 60, 70],
        'Rekomendasi': ['Remedial Math', 'Intensif All', 'Les B. Inggris'],
        'Prioritas': ['Tinggi', 'Tinggi', 'Sedang']
    }
    
    perhatian_df = pd.DataFrame(perhatian_data)
    st.dataframe(perhatian_df)
    
    # Attendance tracking
    st.markdown("---")
    st.subheader("📅 Tracking Kehadiran")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Ketidakhadiran Bulan Ini:**")
        absen_data = {
            'Nama': ['Budi Santoso', 'Maya Sari', 'Andi Wijaya'],
            'Alasan': ['Sakit', 'Izin', 'Sakit'],
            'Hari': [3, 2, 1]
        }
        absen_df = pd.DataFrame(absen_data)
        st.dataframe(absen_df)
    
    with col2:
        st.write("**Keterlambatan:**")
        telat_data = {
            'Nama': ['Riko Pratama', 'Siti Rahma'],
            'Jumlah': [5, 2],
            'Rata-rata': ['10 menit', '5 menit']
        }
        telat_df = pd.DataFrame(telat_data)
        st.dataframe(telat_df)
    
    # Action plan
    st.markdown("---")
    st.subheader("🛠️ Rencana Aksi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Academic Support:**
        - Remedial Matematika (3 siswa)
        - Les B. Inggris (2 siswa)
        - Group study session
        """)
    
    with col2:
        st.warning("""
        **Behavioral Support:**
        - Pertemuan orang tua (2 siswa)
        - Konseling BK (1 siswa)
        - Monitoring kehadiran
        """)
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Hubungi Orang Tua", use_container_width=True):
            st.info("Fitur hubungi orang tua sedang dikembangkan")
    
    with col2:
        if st.button("📝 Catatan Wali", use_container_width=True):
            st.info("Fitur catatan wali sedang dikembangkan")
    
    with col3:
        if st.button("📊 Laporan Kelas", use_container_width=True):
            st.session_state.current_page = "reports"
            st.rerun()

if __name__ == "__main__":
    show_wali_kelas()
