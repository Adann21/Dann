import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_advanced_charts(df, target_col='kelulusan'):
    """
    Fungsi untuk membuat visualisasi data yang advanced
    Menampilkan berbagai jenis chart untuk analisis data
    """
    
    # Set style untuk matplotlib dan seaborn
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. HEATMAP KORELASI
    st.subheader("🔥 Heatmap Korelasi")
    
    # Ambil kolom numerik saja
    kolom_numerik = df.select_dtypes(include=['number']).columns
    
    # Buat heatmap hanya jika ada lebih dari 1 kolom numerik
    if len(kolom_numerik) > 1:
        # Buat figure dan axis untuk matplotlib
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Hitung matrix korelasi
        matrix_korelasi = df[kolom_numerik].corr()
        
        # Buat heatmap menggunakan seaborn
        sns.heatmap(matrix_korelasi, annot=True, cmap='coolwarm', center=0, ax=ax)
        ax.set_title('Peta Korelasi antara Variabel Numerik')
        
        # Tampilkan plot di Streamlit
        st.pyplot(fig)
        
        # Penjelasan interpretasi korelasi
        with st.expander("ℹ️ Cara Membaca Heatmap Korelasi"):
            st.write("""
            - **Warna Merah**: Korelasi positif kuat (mendekati +1)
            - **Warna Biru**: Korelasi negatif kuat (mendekati -1)  
            - **Warna Putih**: Tidak ada korelasi (mendekati 0)
            - Angka menunjukkan nilai korelasi antara -1 sampai +1
            """)
    
    # 2. DISTRIBUSI BERDASARKAN KELULUSAN
    st.subheader("📊 Distribusi berdasarkan Kelulusan")
    
    # Cek apakah kolom target ada dalam dataframe
    if target_col in df.columns:
        # Filter kolom numerik kecuali target
        fitur_numerik = [col for col in kolom_numerik if col != target_col]
        
        if fitur_numerik:
            # Dropdown untuk memilih fitur yang akan dianalisis
            fitur_terpilih = st.selectbox(
                "Pilih fitur untuk dilihat distribusinya:", 
                fitur_numerik
            )
            
            # Buat dua kolom untuk menampilkan histogram dan box plot
            kolom_kiri, kolom_kanan = st.columns(2)
            
            with kolom_kiri:
                # HISTOGRAM
                fig_hist, ax_hist = plt.subplots(figsize=(8, 5))
                
                # Plot histogram untuk setiap status kelulusan
                for status in [0, 1]:
                    data_status = df[df[target_col] == status][fitur_terpilih]
                    label_status = 'Lulus' if status == 1 else 'Tidak Lulus'
                    ax_hist.hist(data_status, alpha=0.7, label=label_status, bins=15)
                
                ax_hist.set_xlabel(fitur_terpilih)
                ax_hist.set_ylabel('Frekuensi')
                ax_hist.legend()
                ax_hist.set_title(f'Distribusi {fitur_terpilih} berdasarkan Kelulusan')
                st.pyplot(fig_hist)
            
            with kolom_kanan:
                # BOX PLOT
                fig_box, ax_box = plt.subplots(figsize=(8, 5))
                
                # Siapkan data untuk box plot
                data_plot = []
                label_plot = []
                
                for status in [0, 1]:
                    data_plot.append(df[df[target_col] == status][fitur_terpilih])
                    label_plot.append('Lulus' if status == 1 else 'Tidak Lulus')
                
                # Buat box plot
                ax_box.boxplot(data_plot, labels=label_plot)
                ax_box.set_ylabel(fitur_terpilih)
                ax_box.set_title(f'Box Plot {fitur_terpilih} berdasarkan Kelulusan')
                st.pyplot(fig_box)
    
    # 3. VISUALISASI INTERAKTIF DENGAN PLOTLY
    st.subheader("📈 Visualisasi Interaktif")
    
    # Chart tingkat kelulusan per kelas
    if 'kelas' in df.columns and target_col in df.columns:
        # Hitung persentase kelulusan per kelas
        tingkat_kelulusan = df.groupby('kelas')[target_col].mean().reset_index()
        tingkat_kelulusan['persentase_lulus'] = tingkat_kelulusan[target_col] * 100
        
        # Buat bar chart interaktif
        fig_bar = px.bar(
            tingkat_kelulusan, 
            x='kelas', 
            y='persentase_lulus',
            title='Tingkat Kelulusan per Kelas',
            labels={
                'persentase_lulus': 'Persentase Lulus (%)', 
                'kelas': 'Kelas'
            },
            color='persentase_lulus',
            color_continuous_scale='viridis'
        )
        
        # Tampilkan chart di Streamlit
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # 4. SCATTER MATRIX
    if len(kolom_numerik) >= 3:
        st.subheader("🔍 Scatter Matrix")
        
        # Pilih 3-4 fitur pertama untuk scatter matrix
        fitur_tampil = kolom_numerik[:4].tolist()
        
        # Buat scatter matrix jika target column ada
        if target_col in df.columns:
            fig_scatter = px.scatter_matrix(
                df,
                dimensions=fitur_tampil,
                color=target_col,
                title="Scatter Matrix of Features",
                labels={str(col): str(col) for col in fitur_tampil}
            )
            
            # Tampilkan scatter matrix
            st.plotly_chart(fig_scatter, use_container_width=True)

def create_prediction_analysis(prediksi, probabilitas, aktual=None):
    """
    Fungsi untuk menganalisis hasil prediksi model
    Menampilkan confusion matrix dan distribusi probabilitas
    """
    
    st.subheader("🔮 Analisis Hasil Prediksi")
    
    # CONFUSION MATRIX (jika ada data aktual)
    if aktual is not None:
        from sklearn.metrics import confusion_matrix, classification_report
        
        # Hitung confusion matrix
        matrix_kebingungan = confusion_matrix(aktual, prediksi)
        
        # Buat heatmap confusion matrix
        fig_cm = px.imshow(
            matrix_kebingungan,
            labels=dict(x="Prediksi", y="Aktual", color="Jumlah"),
            x=['Tidak Lulus', 'Lulus'],
            y=['Tidak Lulus', 'Lulus'],
            title="Confusion Matrix - Matriks Kekeliruan Prediksi"
        )
        
        # Tampilkan confusion matrix
        st.plotly_chart(fig_cm, use_container_width=True)
        
        # Classification report
        st.write("**📋 Laporan Klasifikasi:**")
        laporan = classification_report(aktual, prediksi, output_dict=True)
        df_laporan = pd.DataFrame(laporan).transpose()
        st.dataframe(df_laporan.style.format("{:.2f}"))
    
    # DISTRIBUSI PROBABILITAS
    df_prob = pd.DataFrame({
        'Probabilitas Lulus': probabilitas[:, 1],
        'Prediksi': prediksi
    })
    
    # Buat histogram distribusi probabilitas
    fig_hist_prob = px.histogram(
        df_prob, 
        x='Probabilitas Lulus',
        color='Prediksi',
        nbins=20,
        title='Distribusi Probabilitas Prediksi Kelulusan',
        labels={
            'Probabilitas Lulus': 'Probabilitas', 
            'count': 'Jumlah Siswa'
        }
    )
    
    # Tampilkan histogram probabilitas
    st.plotly_chart(fig_hist_prob, use_container_width=True)

def create_feature_importance_plot(importance_fitur):
    """
    Fungsi untuk membuat plot importance fitur
    Menunjukkan pengaruh setiap variabel terhadap prediksi
    """
    
    st.subheader("🎯 Feature Importance")
    
    # Konversi dictionary importance ke DataFrame
    df_importance = pd.DataFrame({
        'Fitur': list(importance_fitur.keys()),
        'Importance': list(importance_fitur.values())
    }).sort_values('Importance', ascending=True)
    
    # Buat horizontal bar chart
    fig_importance = px.bar(
        df_importance,
        x='Importance',
        y='Fitur',
        orientation='h',
        title='Tingkat Pengaruh Variabel terhadap Prediksi Kelulusan',
        color='Importance',
        color_continuous_scale='reds'
    )
    
    # Update layout untuk tampilan yang lebih baik
    fig_importance.update_layout(
        yaxis={'categoryorder':'total ascending'},
        xaxis_title='Tingkat Importance',
        yaxis_title='Fitur'
    )
    
    # Tampilkan plot importance
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # Penjelasan tentang feature importance
    with st.expander("ℹ️ Penjelasan Feature Importance"):
        st.write("""
        **Feature Importance** menunjukkan seberapa besar pengaruh setiap variabel 
        dalam model prediksi kelulusan:
        
        - **Nilai tinggi**: Fitur sangat berpengaruh dalam menentukan kelulusan
        - **Nilai rendah**: Fitur kurang berpengaruh dalam prediksi
        - Urutan dari atas ke bawah: dari yang paling berpengaruh hingga kurang berpengaruh
        """)