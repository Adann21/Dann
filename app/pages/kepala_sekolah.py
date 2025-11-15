import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.auth import get_current_user, get_current_role

def show_kepala_sekolah():
    user = get_current_user()
    role = get_current_role()
    
    st.title("👑 Dashboard Kepala Sekolah")
    st.markdown(f"**Selamat datang, {user.get('full_name', 'Kepala Sekolah')}!**")
    
    # School overview statistics
    st.markdown("---")
    st.subheader("🏫 Overview Sekolah")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Siswa", "480", "15")
    
    with col2:
        st.metric("Guru & Staff", "45", "2")
    
    with col3:
        st.metric("Rata-rata Nilai", "78.2", "1.5")
    
    with col4:
        st.metric("Tingkat Kelulusan", "92%", "3%")
    
    # Performance by department
    st.markdown("---")
    st.subheader("📊 Performa Jurusan")
    
    jurusan_data = {
        'Jurusan': ['TKJ', 'MM', 'RPL', 'AKL', 'BDP'],
        'Siswa': [120, 95, 110, 85, 70],
        'Rata-rata': [82, 76, 80, 75, 78],
        'Kelulusan': ['94%', '88%', '92%', '90%', '89%'],
        'Rank': [1, 4, 2, 5, 3]
    }
    
    jurusan_df = pd.DataFrame(jurusan_data)
    st.dataframe(jurusan_df)
    
    # Grafik perbandingan jurusan
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Grafik rata-rata nilai
    ax1.bar(jurusan_df['Jurusan'], jurusan_df['Rata-rata'], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    ax1.set_ylabel('Rata-rata Nilai')
    ax1.set_title('Rata-rata Nilai per Jurusan')
    ax1.grid(axis='y', alpha=0.3)
    
    # Grafik tingkat kelulusan
    kelulusan_pct = [int(x.replace('%', '')) for x in jurusan_df['Kelulusan']]
    ax2.bar(jurusan_df['Jurusan'], kelulusan_pct, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    ax2.set_ylabel('Tingkat Kelulusan (%)')
    ax2.set_title('Tingkat Kelulusan per Jurusan')
    ax2.grid(axis='y', alpha=0.3)
    
    st.pyplot(fig)
    
    # Prediksi kelulusan detail
    st.markdown("---")
    st.subheader("🔮 Prediksi Kelulusan Detail")
    
    prediksi_data = {
        'Kelas': ['XII TKJ 1', 'XII TKJ 2', 'XII MM 1', 'XII MM 2', 'XII RPL 1', 'XII RPL 2'],
        'Total': [30, 28, 32, 29, 31, 30],
        'Prediksi Lulus': [25, 24, 28, 25, 27, 26],
        'Prediksi Tidak': [5, 4, 4, 4, 4, 4],
        'Persentase': ['83%', '86%', '88%', '86%', '87%', '87%']
    }
    
    prediksi_df = pd.DataFrame(prediksi_data)
    st.dataframe(prediksi_df)
    
    # Staff performance
    st.markdown("---")
    st.subheader("👥 Performa Guru")
    
    guru_data = {
        'Nama': ['Bu Siti Math', 'Pak Budi TKJ', 'Bu Dewi MM', 'Pak Riko RPL', 'Bu Maya BK'],
        'Bidang': ['Matematika', 'TKJ', 'Multimedia', 'RPL', 'BK'],
        'Rata-rata Nilai': [82, 85, 78, 80, 'N/A'],
        'Siswa Lulus': ['92%', '94%', '88%', '90%', 'N/A'],
        'Rating': ['⭐️⭐️⭐️⭐️⭐️', '⭐️⭐️⭐️⭐️⭐️', '⭐️⭐️⭐️⭐️', '⭐️⭐️⭐️⭐️', '⭐️⭐️⭐️⭐️⭐️']
    }
    
    guru_df = pd.DataFrame(guru_data)
    st.dataframe(guru_df)
    
    # Strategic recommendations
    st.markdown("---")
    st.subheader("💡 Rekomendasi Strategis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("""
        **Area Perbaikan:**
        
        🎯 **Jurusan MM**
        - Tingkatkan rata-rata nilai (saat ini 76)
        - Fokus pada praktikum
        - Upgrade fasilitas lab
        
        🎯 **Siswa Berisiko**
        - 25 siswa perlu perhatian khusus
        - Program remedial intensif
        - Koordinasi orang tua
        """)
    
    with col2:
        st.success("""
        **Kekuatan:**
        
        ✅ **Jurusan TKJ & RPL**
        - Performa sangat baik
        - Tingkat kelulusan tinggi
        - Model untuk jurusan lain
        
        ✅ **Guru Berprestasi**
        - Bu Siti & Pak Budi excellent
        - Berikan apresiasi
        - Jadikan mentor
        """)
    
    # Quick decision panel
    st.markdown("---")
    st.subheader("⚡ Panel Keputusan Cepat")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Lihat Analisis Detail", use_container_width=True):
            st.session_state.current_page = "reports"
            st.rerun()
    
    with col2:
        if st.button("👥 Rapat Koordinasi", use_container_width=True):
            st.info("Fitur rapat koordinasi sedang dikembangkan")
    
    with col3:
        if st.button("📋 Kebijakan Baru", use_container_width=True):
            st.info("Fitur kebijakan sedang dikembangkan")

if __name__ == "__main__":
    show_kepala_sekolah()
