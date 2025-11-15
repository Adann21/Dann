import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

class DataProcessor:
    """
    Kelas untuk memproses data sebelum training model
    Menangani preprocessing, scaling, dan persiapan data
    """
    
    def __init__(self):
        """Inisialisasi DataProcessor dengan scaler dan daftar fitur"""
        # Inisialisasi StandardScaler untuk normalisasi data
        self.scaler = StandardScaler()
        
        # Daftar fitur yang akan digunakan untuk training
        self.daftar_fitur = [
            'nilai_matematika', 
            'nilai_bahasa_indonesia', 
            'nilai_bahasa_inggris',
            'nilai_kejuruan', 
            'kehadiran', 
            'sikap'
        ]
        
        # Kolom target untuk prediksi
        self.kolom_target = 'kelulusan'
    
    def prepare_data(self, dataframe):
        """
        Mempersiapkan data untuk training model
        Membersihkan data dan memisahkan features dengan target
        
        Args:
            dataframe: DataFrame pandas yang berisi data siswa
            
        Returns:
            tuple: (X, y) dimana X adalah features dan y adalah target
            
        Raises:
            ValueError: Jika kolom yang diperlukan tidak ditemukan
            Exception: Jika terjadi error dalam proses preparation
        """
        try:
            # Validasi: pastikan semua kolom yang diperlukan ada dalam dataframe
            for kolom in self.daftar_fitur + [self.kolom_target]:
                if kolom not in dataframe.columns:
                    raise ValueError(f"Kolom {kolom} tidak ditemukan dalam data")
            
            # Handle missing values: hapus baris yang memiliki nilai kosong
            dataframe_clean = dataframe.dropna()
            
            # Pisahkan features (X) dan target (y)
            X = dataframe_clean[self.daftar_fitur]
            y = dataframe_clean[self.kolom_target]
            
            return X, y
            
        except Exception as error:
            raise Exception(f"Error dalam mempersiapkan data: {error}")
    
    def scale_features(self, X, fit=True):
        """
        Melakukan scaling pada fitur menggunakan StandardScaler
        
        Args:
            X: DataFrame atau array yang berisi fitur
            fit: Boolean, apakah melakukan fit transform atau hanya transform
            
        Returns:
            array: Fitur yang sudah di-scale
        """
        if fit:
            # Fit dan transform data (untuk training data)
            return self.scaler.fit_transform(X)
        else:
            # Hanya transform (untuk testing/new data)
            return self.scaler.transform(X)
    
    def save_scaler(self, filepath):
        """
        Menyimpan scaler ke file untuk penggunaan di masa depan
        
        Args:
            filepath: Path lengkap untuk menyimpan file scaler
        """
        joblib.dump(self.scaler, filepath)
    
    def load_scaler(self, filepath):
        """
        Memuat scaler dari file yang sudah disimpan
        
        Args:
            filepath: Path lengkap file scaler yang akan dimuat
        """
        self.scaler = joblib.load(filepath)

# Buat instance global untuk digunakan di seluruh aplikasi
data_processor = DataProcessor()