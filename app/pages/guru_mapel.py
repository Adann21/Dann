import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.auth import get_current_user, get_current_role

def show_guru_mapel():
    user = get_current_user()
    role = get_current_role()
    
    st.title("👨‍🏫 Dashboard Guru Mata Pelajaran")
    st.markdown(f"**Selamat datang, {user.get('full_name', 'Guru')}!**")
    
    # Overview statistics
    st.markdown("---")
    st.subheader("📊 Overview Mengajar")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Siswa", "150", "12")
    
    with col2:
        st.metric("Rata-rata Nilai", "78.5", "2.1")
    
    with col3:
        st.metric("Nilai Tertinggi", "95", "5")
    
    with col4:
        st.metric("Nilai Terendah", "65", "-3")
    
    # Data nilai per kelas
    st.markdown("---")
    st.subheader("📈 Distribusi Nilai per Kelas")
    
    # Sample data
    nilai_data = {
        'Kelas': ['XII TKJ 1', 'XII TKJ 2', 'XII MM 1', 'XII MM 2', 'XII RPL 1'],
        'Rata-rata': [82, 78, 75, 80, 79],
        'Nilai Tertinggi': [95, 92, 88, 94, 90],
        'Nilai Terendah': [70, 65, 62, 68, 66]
    }
    
    nilai_df = pd.DataFrame(nilai_data)
    st.dataframe(nilai_df)
    
    # Grafik distribusi nilai
    fig, ax = plt.subplots(figsize=(10, 6))
    classes = nilai_df['Kelas']
    means = nilai_df['Rata-rata']
    
    ax.bar(classes, means, color='skyblue', alpha=0.7)
    ax.set_ylabel('Rata-rata Nilai')
    ax.set_xlabel('Kelas')
    ax.set_title('Rata-rata Nilai per Kelas')
    ax.grid(axis='y', alpha=0.3)
    
    st.pyplot(fig)
    
    # Analisis siswa butuh perhatian
    st.markdown("---")
    st.subheader("🎯 Siswa Perlu Perhatian")
    
    siswa_data = {
        'Nama': ['Budi Santoso', 'Maya Sari', 'Riko Pratama', 'Siti Rahma'],
        'Kelas': ['XII TKJ 1', 'XII TKJ 2', 'XII MM 1', 'XII MM 2'],
        'Nilai': [65, 62, 68, 70],
        'Status': ['Butuh Remedial', 'Butuh Remedial', 'Perhatian', 'Perhatian']
    }
    
    siswa_df = pd.DataFrame(siswa_data)
    st.dataframe(siswa_df)
    
    # Rekomendasi aksi
    st.markdown("---")
    st.subheader("💡 Rekomendasi Aksi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Untuk Siswa Remedial:**
        - Program remedial intensif
        - Les tambahan
        - Pendekatan individual
        """)
    
    with col2:
        st.info("""
        **Untuk Siswa Perhatian:**
        - Monitoring berkala
        - Motivasi belajar
        - Koordinasi wali kelas
        """)
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Input Nilai", use_container_width=True):
            st.info("Fitur input nilai sedang dikembangkan")
    
    with col2:
        if st.button("📊 Lihat Laporan", use_container_width=True):
            st.session_state.current_page = "reports"
            st.rerun()
    
    with col3:
        if st.button("👥 Koordinasi", use_container_width=True):
            st.info("Fitur koordinasi sedang dikembangkan")

if __name__ == "__main__":
    show_guru_mapel()
