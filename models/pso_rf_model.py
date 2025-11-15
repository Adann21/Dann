import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import streamlit as st

class SimplePSORandomForest:
    """
    Kelas untuk model Random Forest sederhana
    Mengimplementasikan algoritma machine learning untuk prediksi kelulusan siswa
    """
    
    def __init__(self):
        """Inisialisasi model Random Forest sederhana"""
        self.model = None
        self.is_trained = False
        self.feature_importance = None
    
    def train(self, X, y):
        """
        Melakukan training model Random Forest
        
        Args:
            X: Features untuk training (DataFrame atau array)
            y: Target variable untuk training
            
        Returns:
            dict: Hasil training berisi accuracy dan feature importance
        """
        try:
            # Split data menjadi training dan testing set
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Inisialisasi model Random Forest
            self.model = RandomForestClassifier(
                n_estimators=100,      # Jumlah tree dalam forest
                max_depth=10,          # Kedalaman maksimum setiap tree
                random_state=42,       # Seed untuk reproducibility
                n_jobs=-1              # Gunakan semua core processor
            )
            
            # Training model dengan data training
            self.model.fit(X_train, y_train)
            
            # Evaluasi model dengan data testing
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Hitung feature importance
            self.feature_importance = dict(zip(X.columns, self.model.feature_importances_))
            
            # Set status model menjadi trained
            self.is_trained = True
            
            # Return hasil training
            return {
                'accuracy': accuracy,
                'feature_importance': self.feature_importance,
                'model': self.model
            }
            
        except Exception as error:
            st.error(f"❌ Error training model: {error}")
            return None
    
    def predict(self, X):
        """
        Melakukan prediksi menggunakan model yang sudah ditraining
        
        Args:
            X: Data features yang akan diprediksi
            
        Returns:
            tuple: predictions dan probabilities
            
        Raises:
            Exception: Jika model belum ditraining
        """
        if not self.is_trained or self.model is None:
            raise Exception("Model belum di-training! Silakan train model terlebih dahulu.")
        
        # Lakukan prediksi
        predictions = self.model.predict(X)
        
        # Dapatkan probabilities untuk setiap kelas
        probabilities = self.model.predict_proba(X)
        
        return predictions, probabilities
    
    def save_model(self, filepath):
        """
        Menyimpan model ke file menggunakan joblib
        
        Args:
            filepath: Path lengkap untuk menyimpan file model
        """
        if self.model is not None:
            joblib.dump(self.model, filepath)
            st.success(f"✅ Model berhasil disimpan di: {filepath}")
        else:
            st.warning("⚠️ Tidak ada model yang dapat disimpan")
    
    def load_model(self, filepath):
        """
        Memuat model dari file yang sudah disimpan
        
        Args:
            filepath: Path lengkap file model yang akan dimuat
        """
        try:
            self.model = joblib.load(filepath)
            self.is_trained = True
            st.success("✅ Model berhasil dimuat")
        except Exception as error:
            st.error(f"❌ Error memuat model: {error}")

# Buat instance global untuk digunakan di seluruh aplikasi
pso_rf_model = SimplePSORandomForest()