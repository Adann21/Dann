import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
from app.auth import get_current_user, get_current_role
from models.pso_rf_model import pso_rf_model
from app.visualizations import create_prediction_analysis, create_feature_importance_plot

def show_reports():
    user = get_current_user()
    role = get_current_role()
    
    st.title("📋 Laporan Prediksi Kelulusan")
    st.markdown(f"**Login sebagai:** {role.replace('_', ' ').title()}")
    
    # Check if data and model exist
    if 'data_siswa' not in st.session_state:
        st.warning("⚠️ Silakan upload data siswa terlebih dahulu di menu Dashboard")
        return
    
    if not st.session_state.get('model_trained', False):
        st.warning("⚠️ Silakan train model terlebih dahulu di menu Prediksi")
        return
    
    df = st.session_state.data_siswa
    model_results = st.session_state.model_results
    
    # Generate predictions for all data
    try:
        from models.data_processor import data_processor
        X, y = data_processor.prepare_data(df)
        predictions, probabilities = pso_rf_model.predict(X)
        
        # Add predictions to dataframe
        df_pred = df.copy()
        df_pred['prediksi_kelulusan'] = predictions
        df_pred['probabilitas_lulus'] = probabilities[:, 1]
        df_pred['probabilitas_tidak_lulus'] = probabilities[:, 0]
        df_pred['kategori_risiko'] = np.where(
            probabilities[:, 1] > 0.8, 'Rendah',
            np.where(probabilities[:, 1] > 0.6, 'Sedang', 'Tinggi')
        )
        
        st.session_state.df_with_predictions = df_pred
        
    except Exception as e:
        st.error(f"❌ Error generating predictions: {e}")
        return
    
    # Analysis Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ringkasan", "🎯 Analisis", "📋 Detail", "📤 Export"])
    
    with tab1:
        st.subheader("📊 Ringkasan Laporan")
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_siswa = len(df_pred)
        prediksi_lulus = df_pred['prediksi_kelulusan'].sum()
        prediksi_tidak_lulus = total_siswa - prediksi_lulus
        persentase_lulus = (prediksi_lulus / total_siswa) * 100
        
        with col1:
            st.metric("Total Siswa", total_siswa)
        
        with col2:
            st.metric("Prediksi Lulus", prediksi_lulus)
        
        with col3:
            st.metric("Prediksi Tidak Lulus", prediksi_tidak_lulus)
        
        with col4:
            st.metric("Persentase Lulus", f"{persentase_lulus:.1f}%")
        
        # Risk analysis
        st.subheader("⚠️ Analisis Risiko")
        risk_counts = df_pred['kategori_risiko'].value_counts()
        
        risk_col1, risk_col2, risk_col3 = st.columns(3)
        
        with risk_col1:
            st.metric("Risiko Tinggi", risk_counts.get('Tinggi', 0))
        
        with risk_col2:
            st.metric("Risiko Sedang", risk_counts.get('Sedang', 0))
        
        with risk_col3:
            st.metric("Risiko Rendah", risk_counts.get('Rendah', 0))
    
    with tab2:
        st.subheader("🎯 Analisis Mendalam")
        
        # Feature Importance
        create_feature_importance_plot(model_results['feature_importance'])
        
        # Prediction Analysis
        create_prediction_analysis(predictions, probabilities, y)
        
        # Recommendations based on analysis
        st.subheader("💡 Rekomendasi Strategis")
        
        if prediksi_tidak_lulus > 0:
            st.warning(f"""
            **⚠️ PERHATIAN: {prediksi_tidak_lulus} SISWA BERISIKO TIDAK LULUS**
            
            **Rekomendasi:**
            1. **Program Remedial Intensif** untuk {prediksi_tidak_lulus} siswa berisiko
            2. **Fokus pada fitur penting**: {list(model_results['feature_importance'].keys())[:2]}
            3. **Monitoring berkala** untuk siswa dengan probabilitas < 60%
            4. **Koordinasi orang tua** untuk siswa risiko tinggi
            """)
        else:
            st.success("""
            **🎉 SEMUA SISWA DIPREDIKSI LULUS!**
            
            **Langkah selanjutnya:**
            1. Pertahankan kualitas pembelajaran
            2. Monitor siswa dengan probabilitas rendah
            3. Siapkan program pengayaan
            """)
    
    with tab3:
        st.subheader("📋 Detail Prediksi per Siswa")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_kelas = st.multiselect(
                "Filter Kelas:",
                options=df_pred['kelas'].unique(),
                default=df_pred['kelas'].unique()
            )
        
        with col2:
            filter_prediksi = st.multiselect(
                "Filter Prediksi:",
                options=['LULUS', 'TIDAK LULUS'],
                default=['LULUS', 'TIDAK LULUS']
            )
        
        with col3:
            filter_risiko = st.multiselect(
                "Filter Risiko:",
                options=['Tinggi', 'Sedang', 'Rendah'],
                default=['Tinggi', 'Sedang', 'Rendah']
            )
        
        # Apply filters
        filtered_df = df_pred[df_pred['kelas'].isin(filter_kelas)]
        filtered_df = filtered_df[filtered_df['kategori_risiko'].isin(filter_risiko)]
        
        if 'LULUS' in filter_prediksi and 'TIDAK LULUS' not in filter_prediksi:
            filtered_df = filtered_df[filtered_df['prediksi_kelulusan'] == 1]
        elif 'TIDAK LULUS' in filter_prediksi and 'LULUS' not in filter_prediksi:
            filtered_df = filtered_df[filtered_df['prediksi_kelulusan'] == 0]
        
        # Display filtered data with styling
        display_df = filtered_df[[
            'nis', 'nama', 'kelas', 'nilai_matematika', 'nilai_bahasa_indonesia',
            'nilai_bahasa_inggris', 'nilai_kejuruan', 'kehadiran', 'sikap',
            'prediksi_kelulusan', 'probabilitas_lulus', 'kategori_risiko'
        ]].rename(columns={
            'prediksi_kelulusan': 'Prediksi',
            'probabilitas_lulus': 'Prob Lulus',
            'kategori_risiko': 'Risiko'
        })
        
        # Format the dataframe
        styled_df = display_df.style.format({
            'Prob Lulus': '{:.2%}'
        }).apply(
            lambda x: ['background-color: #d4edda' if x['Prediksi'] == 1 else 'background-color: #f8d7da' for _ in x],
            axis=1
        )
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Show filtered count
        st.info(f"Menampilkan {len(filtered_df)} dari {total_siswa} siswa")
    
    with tab4:
        st.subheader("📤 Export Laporan")
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            # Export to CSV
            csv_data = df_pred.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV Lengkap",
                data=csv_data,
                file_name=f"laporan_prediksi_lengkap_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Export filtered data
            filtered_csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Data Terfilter",
                data=filtered_csv,
                file_name=f"laporan_terfilter_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Export summary report
            summary_report = f"""
LAPORAN PREDIKSI KELULUSAN - SMKN 1 SANDAI
===========================================
Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Dibuat oleh: {user.get('full_name', 'System')}

STATISTIK UTAMA:
----------------
- Total Siswa: {total_siswa}
- Prediksi Lulus: {prediksi_lulus}
- Prediksi Tidak Lulus: {prediksi_tidak_lulus}
- Persentase Kelulusan: {persentase_lulus:.1f}%
- Akurasi Model: {model_results['accuracy']:.2%}

ANALISIS RISIKO:
----------------
- Risiko Tinggi: {risk_counts.get('Tinggi', 0)} siswa
- Risiko Sedang: {risk_counts.get('Sedang', 0)} siswa  
- Risiko Rendah: {risk_counts.get('Rendah', 0)} siswa

FEATURE IMPORTANCE (Top 3):
---------------------------
{list(model_results['feature_importance'].keys())[0]}: {list(model_results['feature_importance'].values())[0]:.3f}
{list(model_results['feature_importance'].keys())[1]}: {list(model_results['feature_importance'].values())[1]:.3f}
{list(model_results['feature_importance'].keys())[2]}: {list(model_results['feature_importance'].values())[2]:.3f}

REKOMENDASI:
------------
{f"1. Fokus pada {prediksi_tidak_lulus} siswa berisiko tidak lulus" if prediksi_tidak_lulus > 0 else "1. Pertahankan performa saat ini"}
2. Tingkatkan {list(model_results['feature_importance'].keys())[0]} dan {list(model_results['feature_importance'].keys())[1]}
3. Monitor siswa dengan probabilitas di bawah 60%
4. Lakukan evaluasi berkala

Catatan: Laporan ini dihasilkan otomatis oleh Sistem Prediksi Kelulusan SMKN 1 Sandai.
            """
            
            st.download_button(
                label="📄 Download Summary Report",
                data=summary_report,
                file_name=f"summary_laporan_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Model performance file
            model_perf = f"""
PERFORMANCE MODEL:
------------------
Algorithm: Random Forest
Accuracy: {model_results['accuracy']:.4f}
Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FEATURE IMPORTANCE:
-------------------
"""
            for feature, importance in model_results['feature_importance'].items():
                model_perf += f"{feature}: {importance:.4f}\n"
            
            st.download_button(
                label="🤖 Download Model Info",
                data=model_perf,
                file_name=f"model_performance_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    show_reports()
