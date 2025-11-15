import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class EnhancedPSORandomForest:
    """
    Kelas untuk model Random Forest yang dioptimasi dengan PSO (Particle Swarm Optimization)
    Meningkatkan performa model dengan optimasi hyperparameter otomatis
    """
    
    def __init__(self):
        """Inisialisasi model Enhanced PSO Random Forest"""
        self.model = None
        self.is_trained = False
        self.feature_importance = None
        self.scaler = StandardScaler()
        self.best_params = None
        self.cv_scores = None
    
    def pso_optimization(self, X, y, n_particles=10, max_iter=20):
        """
        Melakukan optimasi hyperparameter menggunakan PSO
        
        Args:
            X: Features untuk training
            y: Target variable
            n_particles: Jumlah partikel dalam PSO
            max_iter: Jumlah maksimum iterasi
            
        Returns:
            tuple: Best parameters dan best score
        """
        st.info("🔧 Menjalankan PSO Optimization...")
        
        # Batas parameter untuk optimasi [n_estimators, max_depth, min_samples_split]
        batas_parameter = np.array([[50, 200], [5, 20], [2, 10]])
        
        # Inisialisasi partikel secara random dalam batas yang ditentukan
        partikel = np.random.uniform(
            batas_parameter[:, 0], batas_parameter[:, 1], 
            (n_particles, len(batas_parameter))
        ).astype(int)
        
        kecepatan = np.zeros_like(partikel)
        best_personal = partikel.copy()
        skor_best_personal = np.zeros(n_particles)
        
        best_global = None
        skor_best_global = -np.inf
        
        # Setup progress bar untuk monitoring
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Loop iterasi PSO
        for iterasi in range(max_iter):
            skor_iterasi = []
            
            for i, particle in enumerate(partikel):
                try:
                    # Ekstrak parameter dari partikel
                    n_estimators, max_depth, min_samples_split = particle
                    
                    # Buat model dengan parameter saat ini
                    model_sementara = RandomForestClassifier(
                        n_estimators=int(n_estimators),
                        max_depth=int(max_depth),
                        min_samples_split=int(min_samples_split),
                        random_state=42,
                        n_jobs=-1
                    )
                    
                    # Hitung cross validation score
                    skor_cv = np.mean(cross_val_score(model_sementara, X, y, cv=3, scoring='accuracy'))
                    skor_iterasi.append(skor_cv)
                    
                    # Update best personal
                    if skor_cv > skor_best_personal[i]:
                        best_personal[i] = particle
                        skor_best_personal[i] = skor_cv
                    
                    # Update best global
                    if skor_cv > skor_best_global:
                        best_global = particle.copy()
                        skor_best_global = skor_cv
                        
                except Exception as error:
                    # Jika error, beri skor 0
                    skor_iterasi.append(0)
            
            # Update kecepatan dan posisi partikel
            w = 0.7  # inertia weight
            c1 = 1.5  # cognitive parameter
            c2 = 1.5  # social parameter
            
            r1 = np.random.random(partikel.shape)
            r2 = np.random.random(partikel.shape)
            
            kecepatan = (w * kecepatan + 
                        c1 * r1 * (best_personal - partikel) + 
                        c2 * r2 * (best_global - partikel))
            
            partikel = partikel + kecepatan.astype(int)
            
            # Pastikan partikel tetap dalam batas
            for dimensi in range(len(batas_parameter)):
                partikel[:, dimensi] = np.clip(partikel[:, dimensi], 
                                             batas_parameter[dimensi, 0], 
                                             batas_parameter[dimensi, 1])
            
            # Update progress bar
            progress = (iterasi + 1) / max_iter
            progress_bar.progress(progress)
            status_text.text(f"Iterasi {iterasi + 1}/{max_iter} - Best Score: {skor_best_global:.4f}")
        
        # Clear progress bar setelah selesai
        progress_bar.empty()
        status_text.empty()
        
        return best_global, skor_best_global
    
    def train_enhanced(self, X, y, use_pso=True):
        """
        Training model dengan atau tanpa optimasi PSO
        
        Args:
            X: Features untuk training
            y: Target variable
            use_pso: Boolean apakah menggunakan PSO atau tidak
            
        Returns:
            dict: Hasil evaluasi model
        """
        try:
            # Scale features untuk konsistensi
            X_scaled = self.scaler.fit_transform(X)
            
            if use_pso:
                # Optimasi parameter dengan PSO
                best_params, best_score = self.pso_optimization(X_scaled, y)
                
                n_estimators, max_depth, min_samples_split = best_params
                
                self.model = RandomForestClassifier(
                    n_estimators=int(n_estimators),
                    max_depth=int(max_depth),
                    min_samples_split=int(min_samples_split),
                    random_state=42,
                    n_jobs=-1
                )
                
                self.best_params = {
                    'n_estimators': int(n_estimators),
                    'max_depth': int(max_depth),
                    'min_samples_split': int(min_samples_split)
                }
                
            else:
                # Gunakan parameter default
                self.model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    n_jobs=-1
                )
                self.best_params = {'n_estimators': 100, 'max_depth': 10, 'min_samples_split': 2}
            
            # Split data untuk training dan testing
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Training model
            self.model.fit(X_train, y_train)
            
            # Evaluasi model
            y_pred = self.model.predict(X_test)
            akurasi = accuracy_score(y_test, y_pred)
            
            # Cross validation scores
            self.cv_scores = cross_val_score(self.model, X_scaled, y, cv=5, scoring='accuracy')
            
            # Feature importance
            self.feature_importance = dict(zip(X.columns, self.model.feature_importances_))
            
            self.is_trained = True
            
            return {
                'accuracy': akurasi,
                'cv_mean': np.mean(self.cv_scores),
                'cv_std': np.std(self.cv_scores),
                'feature_importance': self.feature_importance,
                'best_params': self.best_params,
                'confusion_matrix': confusion_matrix(y_test, y_pred),
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
            
        except Exception as error:
            st.error(f"❌ Error training enhanced model: {error}")
            return None
    
    def predict_enhanced(self, X):
        """
        Melakukan prediksi dengan model yang sudah ditraining
        
        Args:
            X: Data features untuk diprediksi
            
        Returns:
            tuple: Predictions dan probabilities
            
        Raises:
            Exception: Jika model belum ditraining
        """
        if not self.is_trained or self.model is None:
            raise Exception("Model belum di-training!")
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        return predictions, probabilities
    
    def create_model_dashboard(self):
        """
        Membuat dashboard visualisasi performa model
        
        Returns:
            plotly.graph_objects.Figure: Figure dashboard
        """
        if not self.is_trained:
            return None
        
        # Buat subplots untuk dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Feature Importance', 'CV Scores Distribution', 
                          'Confusion Matrix', 'Parameters'),
            specs=[[{"type": "bar"}, {"type": "box"}],
                   [{"type": "heatmap"}, {"type": "table"}]]
        )
        
        # Feature Importance plot
        features = list(self.feature_importance.keys())
        importances = list(self.feature_importance.values())
        
        fig.add_trace(
            go.Bar(x=importances, y=features, orientation='h', name='Importance'),
            row=1, col=1
        )
        
        # CV Scores distribution
        fig.add_trace(
            go.Box(y=self.cv_scores, name='CV Scores', boxpoints='all'),
            row=1, col=2
        )
        
        # Parameters table
        fig.add_trace(
            go.Table(
                header=dict(values=['Parameter', 'Value']),
                cells=dict(values=[list(self.best_params.keys()), 
                                 list(self.best_params.values())])
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, title_text="Model Performance Dashboard")
        return fig
    
    def save_enhanced_model(self, filepath):
        """
        Menyimpan model dan scaler ke file
        
        Args:
            filepath: Path untuk menyimpan model
        """
        if self.model is not None:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'best_params': self.best_params,
                'feature_importance': self.feature_importance
            }
            joblib.dump(model_data, filepath)
    
    def load_enhanced_model(self, filepath):
        """
        Memuat model dan scaler dari file
        
        Args:
            filepath: Path file model yang akan dimuat
        """
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.best_params = model_data['best_params']
        self.feature_importance = model_data['feature_importance']
        self.is_trained = True

# Buat instance global untuk digunakan di seluruh aplikasi
enhanced_pso_rf = EnhancedPSORandomForest()