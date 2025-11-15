import streamlit as st
import pandas as pd
import numpy as np
from app.auth import get_current_user, get_current_role
from models.data_processor import data_processor
from models.pso_rf_model import pso_rf_model

def show_prediction():
    user = get_current_user()
    role = get_current_role()
    
    st.title("🔮 Prediksi Kelulusan Siswa")
    st.markdown(f"**Login sebagai:** {role.replace('_', ' ').title()}")
    
    # Check if data exists in session
    if 'data_siswa' not in st.session_state:
        st.warning("⚠️ Silakan upload data siswa terlebih dahulu di menu Dashboard")
        return
    
    df = st.session_state.data_siswa
    
    # Training section
    st.markdown("---")
    st.subheader("🤖 Training Model Prediksi")
    
    if st.button("🚀 Train Model Random Forest", type="primary"):
        with st.spinner("Training model..."):
            try:
                # Prepare data
                X, y = data_processor.prepare_data(df)
                
                # Train model
                result = pso_rf_model.train(X, y)
                
                if result:
                    st.session_state.model_trained = True
                    st.session_state.model_results = result
                    
                    st.success("✅ Model berhasil di-training!")
                    
                    # Show results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Akurasi Model", f"{result['accuracy']:.2%}")
                    
                    with col2:
                        st.metric("Status", "Trained")
                    
                    # Feature importance
                    st.subheader("📊 Feature Importance")
                    importance_df = pd.DataFrame({
                        'Feature': list(result['feature_importance'].keys()),
                        'Importance': list(result['feature_importance'].values())
                    }).sort_values('Importance', ascending=False)
                    
                    st.dataframe(importance_df)
                    
            except Exception as e:
                st.error(f"❌ Error training model: {e}")
    
    # Prediction section
    if st.session_state.get('model_trained', False):
        st.markdown("---")
        st.subheader("🎯 Prediksi Data Baru")
        
        # Input form untuk prediksi manual
        st.write("**Input Data Siswa untuk Prediksi:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            matematika = st.number_input("Nilai Matematika", 0, 100, 75)
            bahasa_inggris = st.number_input("Nilai Bahasa Inggris", 0, 100, 75)
        
        with col2:
            bahasa_indonesia = st.number_input("Nilai Bahasa Indonesia", 0, 100, 75)
            kejuruan = st.number_input("Nilai Kejuruan", 0, 100, 80)
        
        with col3:
            kehadiran = st.number_input("Persentase Kehadiran", 0, 100, 85)
            sikap = st.number_input("Nilai Sikap", 0, 100, 85)
        
        if st.button("🔍 Prediksi Kelulusan"):
            try:
                # Create input data
                input_data = pd.DataFrame([{
                    'nilai_matematika': matematika,
                    'nilai_bahasa_indonesia': bahasa_indonesia,
                    'nilai_bahasa_inggris': bahasa_inggris,
                    'nilai_kejuruan': kejuruan,
                    'kehadiran': kehadiran,
                    'sikap': sikap
                }])
                
                # Predict
                predictions, probabilities = pso_rf_model.predict(input_data)
                
                # Display results
                pred = predictions[0]
                prob = probabilities[0]
                
                st.markdown("---")
                st.subheader("📋 Hasil Prediksi")
                
                if pred == 1:
                    st.success(f"🎉 **PREDIKSI: LULUS**")
                    st.write(f"Probabilitas Lulus: {prob[1]:.2%}")
                    st.write(f"Probabilitas Tidak Lulus: {prob[0]:.2%}")
                else:
                    st.error(f"❌ **PREDIKSI: TIDAK LULUS**")
                    st.write(f"Probabilitas Lulus: {prob[1]:.2%}")
                    st.write(f"Probabilitas Tidak Lulus: {prob[0]:.2%}")
                
                # Recommendation
                st.info("💡 **Rekomendasi:** Fokus pada mata pelajaran dengan importance tertinggi untuk meningkatkan peluang kelulusan")
                
            except Exception as e:
                st.error(f"❌ Error melakukan prediksi: {e}")
    
    else:
        st.info("ℹ️ Train model terlebih dahulu untuk melakukan prediksi")

if __name__ == "__main__":
    show_prediction()
