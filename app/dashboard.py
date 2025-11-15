import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.auth import get_current_user, get_current_role
from app.visualizations import create_advanced_charts

def show_dashboard():
    user = get_current_user()
    role = get_current_role()
    
    st.title("📊 Dashboard Analisis Data Siswa")
    st.markdown(f"**Login sebagai:** {role.replace('_', ' ').title()}")
    
    # Template download section
    st.markdown("### 📥 Download Template Data Siswa")
    
    # Buat template DataFrame
    template_data = {
        'nis': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'nama': ['Nama Siswa 1', 'Nama Siswa 2', 'Nama Siswa 3', 'Nama Siswa 4', 'Nama Siswa 5'],
        'kelas': ['XII TKJ 1', 'XII TKJ 1', 'XII MM 1', 'XII MM 1', 'XII RPL 1'],
        'nilai_matematika': [85, 78, 92, 65, 88],
        'nilai_bahasa_indonesia': [80, 75, 85, 70, 82],
        'nilai_bahasa_inggris': [78, 82, 79, 68, 85],
        'nilai_kejuruan': [90, 85, 88, 72, 89],
        'kehadiran': [95, 88, 92, 85, 96],
        'sikap': [90, 85, 88, 80, 92],
        'kelulusan': [1, 1, 1, 0, 1]  # 1 = Lulus, 0 = Tidak Lulus
    }
    
    template_df = pd.DataFrame(template_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tampilkan preview template
        st.markdown("**Preview Template:**")
        st.dataframe(template_df.head(3))
        
        # Download button untuk template
        csv_template = template_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Template CSV",
            data=csv_template,
            file_name="template_data_siswa.csv",
            mime="text/csv",
            help="Download template ini, isi dengan data siswa yang sebenarnya, lalu upload kembali"
        )
    
    with col2:
        st.markdown("**📋 Petunjuk Pengisian:**")
        st.markdown("""
        - **nis**: Nomor Induk Siswa (unik)
        - **nama**: Nama lengkap siswa
        - **kelas**: Kelas siswa (XII TKJ 1, XII MM 2, dll)
        - **nilai_***: Nilai 0-100
        - **kehadiran**: Persentase kehadiran 0-100
        - **sikap**: Nilai sikap 0-100  
        - **kelulusan**: 1 = Lulus, 0 = Tidak Lulus
        """)
    
   # Upload data section
    st.markdown("---")
    st.subheader("📤 Upload Data Siswa")
    
    # File uploader
    uploaded_file = st.file_uploader("Pilih file CSV data siswa yang sudah diisi", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.data_siswa = df
            
            # Validasi kolom yang diperlukan
            required_columns = ['nis', 'nama', 'kelas', 'nilai_matematika', 'nilai_bahasa_indonesia', 
                              'nilai_bahasa_inggris', 'nilai_kejuruan', 'kehadiran', 'sikap']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Kolom berikut tidak ditemukan: {', '.join(missing_columns)}")
                st.info("💡 Gunakan template yang disediakan untuk format yang benar")
            else:
                st.success(f"✅ Data berhasil diupload! {len(df)} records ditemukan.")
                
                # Tampilkan preview data
                st.subheader("👀 Preview Data")
                st.dataframe(df.head(10))
                
                # Basic Information
                st.subheader("📈 Informasi Data")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Siswa", len(df))
                
                with col2:
                    st.metric("Total Kelas", df['kelas'].nunique())
                
                with col3:
                    numeric_cols = len(df.select_dtypes(include=['number']).columns)
                    st.metric("Fitur Numerik", numeric_cols)
                
                with col4:
                    if 'kelulusan' in df.columns:
                        lulus_count = df['kelulusan'].sum()
                        st.metric("Data Label Kelulusan", f"{lulus_count}/{len(df)}")
                    else:
                        st.metric("Data Label Kelulusan", "Tidak Ada")
                
                # Data types
                st.write("**🔧 Tipe Data:**")
                dtype_df = pd.DataFrame(df.dtypes, columns=['Tipe Data']).reset_index()
                dtype_df.columns = ['Kolom', 'Tipe Data']
                st.dataframe(dtype_df)
                
                # ✅ BUTTON SIMPAN KE DATABASE - DITEMPATKAN DI SINI
                if st.button("💾 Simpan Data ke Database", type="primary"):
                    try:
                        # Simpan ke database PostgreSQL
                        from models.database import db
                        
                        with db.koneksi.cursor() as cursor:
                            for _, row in df.iterrows():
                                cursor.execute("""
                                    INSERT INTO students 
                                    (nis, nama, kelas, nilai_matematika, nilai_bahasa_indonesia, 
                                     nilai_bahasa_inggris, nilai_kejuruan, kehadiran, sikap, kelulusan)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (nis) DO UPDATE SET
                                    nama = EXCLUDED.nama,
                                    kelas = EXCLUDED.kelas,
                                    nilai_matematika = EXCLUDED.nilai_matematika,
                                    nilai_bahasa_indonesia = EXCLUDED.nilai_bahasa_indonesia,
                                    nilai_bahasa_inggris = EXCLUDED.nilai_bahasa_inggris,
                                    nilai_kejuruan = EXCLUDED.nilai_kejuruan,
                                    kehadiran = EXCLUDED.kehadiran,
                                    sikap = EXCLUDED.sikap,
                                    kelulusan = EXCLUDED.kelulusan
                                """, (
                                    row['nis'], row['nama'], row['kelas'],
                                    row['nilai_matematika'], row['nilai_bahasa_indonesia'],
                                    row['nilai_bahasa_inggris'], row['nilai_kejuruan'],
                                    row['kehadiran'], row['sikap'], 
                                    row.get('kelulusan')  # Opsional
                                ))
                            
                            db.koneksi.commit()
                            st.success(f"✅ Data {len(df)} siswa berhasil disimpan ke database!")
                            st.balloons()
                            
                    except Exception as e:
                        st.error(f"❌ Error menyimpan data ke database: {e}")
                
                # Advanced Visualizations
                st.markdown("---")
                create_advanced_charts(df)
            
        except Exception as e:
            st.error(f"❌ Error membaca file: {e}")
            st.info("💡 Pastikan file CSV sesuai dengan template yang disediakan")
    
    else:
        st.info("ℹ️ Silakan download template, isi dengan data siswa, lalu upload file CSV yang sudah diisi")

# Jalankan halaman jika file di-execute langsung
if __name__ == "__main__":
    show_dashboard()