import streamlit as st
import sys
import os
import pandas as pd
import numpy as np

# Tambahkan project root ke path untuk import modul
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth import check_authentication, logout, get_current_role
from app.pages.beranda import show as show_beranda
from app.dashboard import show_dashboard
from app.pages.prediction import show_prediction
from app.pages.advanced_prediction import show_advanced_prediction
from app.pages.reports import show_reports
from app.user_management import show_user_management
from app.pages.kepala_sekolah import show_kepala_sekolah
from app.pages.guru_mapel import show_guru_mapel
from app.pages.guru_bk import show_guru_bk
from app.pages.wali_kelas import show_wali_kelas
from utils.constants.permissions import ROLE_PERMISSIONS

def load_css():
    """
    Fungsi untuk memuat custom CSS
    Jika file CSS tidak ditemukan, aplikasi tetap berjalan tanpa CSS
    """
    try:
        # Baca file CSS dari folder static
        with open('static/css/style.css') as css_file:
            st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Jika file CSS tidak ada, lanjutkan tanpa CSS
        pass

def main():
    """
    Fungsi utama aplikasi Streamlit
    Menangani konfigurasi halaman, autentikasi, dan navigasi
    """
    # Konfigurasi halaman Streamlit
    st.set_page_config(
        page_title="Sistem Prediksi Kelulusan - SMKN 1 Sandai",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Muat custom CSS
    load_css()
    
    # Inisialisasi session state untuk status model
    if 'model_trained' not in st.session_state:
        st.session_state.model_trained = False
    if 'advanced_model_trained' not in st.session_state:
        st.session_state.advanced_model_trained = False
    
    # Cek autentikasi user, jika belum login akan berhenti di sini
    check_authentication()
    
    # Ambil role user yang sedang login
    user_role = get_current_role()
    
    # Sidebar navigation
    with st.sidebar:
        # Header sidebar
        st.title("SMKN 1 Sandai")
        st.markdown("---")
        
        # Dapatkan permissions berdasarkan role user
        user_permissions = ROLE_PERMISSIONS.get(user_role, {})
        
        # SECTION MENU UTAMA
        st.subheader("📋 Menu Utama")
        
        # Tombol Beranda - selalu tersedia untuk semua role
        if st.button("🏠 Beranda", use_container_width=True, 
                    type="primary" if st.session_state.get('current_page') == 'beranda' else "secondary"):
            st.session_state.current_page = "beranda"
            st.rerun()
        
        # Tombol Dashboard - berdasarkan permissions
        if user_permissions.get("dashboard", False):
            if st.button("📊 Dashboard", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'dashboard' else "secondary"):
                st.session_state.current_page = "dashboard"
                st.rerun()
        
        # SECTION PREDIKSI
        if user_permissions.get("prediction", False):
            st.subheader("🔮 Prediksi")
            
            # Tombol Basic Prediction
            if st.button("📈 Basic Prediction", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'prediction' else "secondary"):
                st.session_state.current_page = "prediction"
                st.rerun()
            
            # Tombol Advanced Prediction
            if st.button("📊 Advanced Prediction", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'advanced_prediction' else "secondary"):
                st.session_state.current_page = "advanced_prediction"
                st.rerun()
        
        # Tombol Laporan - berdasarkan permissions
        if user_permissions.get("reports", False):
            if st.button("📑 Laporan", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'reports' else "secondary"):
                st.session_state.current_page = "reports"
                st.rerun()
        
        # SECTION ADMIN - hanya untuk role tertentu
        if user_permissions.get("user_management", False):
            st.subheader("⚙️ Admin")
            if st.button("👥 Manage Users", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'user_management' else "secondary"):
                st.session_state.current_page = "user_management"
                st.rerun()
        
        # DASHBOARD ROLE-SPECIFIC
        # Dashboard khusus Kepala Sekolah
        if user_role == "kepala_sekolah":
            if st.button("👑 Dashboard KS", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'kepala_sekolah' else "secondary"):
                st.session_state.current_page = "kepala_sekolah"
                st.rerun()
        
        # Dashboard khusus Guru Mata Pelajaran
        elif user_role == "guru_mapel":
            if st.button("📚 Dashboard Guru", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'guru_mapel' else "secondary"):
                st.session_state.current_page = "guru_mapel"
                st.rerun()
        
        # Dashboard khusus Guru BK
        elif user_role == "guru_bk":
            if st.button("💬 Dashboard BK", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'guru_bk' else "secondary"):
                st.session_state.current_page = "guru_bk"
                st.rerun()
        
        # Dashboard khusus Wali Kelas
        elif user_role == "wali_kelas":
            if st.button("🏫 Dashboard Wali", use_container_width=True, 
                        type="primary" if st.session_state.get('current_page') == 'wali_kelas' else "secondary"):
                st.session_state.current_page = "wali_kelas"
                st.rerun()
        
        st.markdown("---")
        
        # INFO STATUS SAAT INI
        # Tampilkan halaman aktif saat ini
        current_active_page = st.session_state.get('current_page', 'beranda')
        
        # Mapping nama halaman untuk display
        nama_halaman = {
            'beranda': 'Beranda',
            'dashboard': 'Dashboard', 
            'prediction': 'Basic Prediction',
            'advanced_prediction': 'Advanced Prediction',
            'reports': 'Laporan',
            'user_management': 'Manage Users',
            'kepala_sekolah': 'Dashboard KS',
            'guru_mapel': 'Dashboard Guru',
            'guru_bk': 'Dashboard BK',
            'wali_kelas': 'Dashboard Wali'
        }
        
        # Tampilkan informasi halaman aktif dan role
        st.caption(f"📍 Halaman Aktif: {nama_halaman.get(current_active_page, 'Beranda')}")
        
        # Format role untuk display (hapus underscore dan kapitalisasi)
        role_display = user_role.replace('_', ' ').title()
        st.caption(f"👤 Role: {role_display}")
        
        st.markdown("---")
        
        # Tombol logout
        logout()
    
    # AREA KONTEN UTAMA
    # Tentukan halaman mana yang akan ditampilkan berdasarkan session state
    current_active_page = st.session_state.get("current_page", "beranda")
    
    # Routing ke halaman yang sesuai
    if current_active_page == "beranda":
        show_beranda()
    elif current_active_page == "dashboard":
        show_dashboard()
    elif current_active_page == "prediction":
        show_prediction()
    elif current_active_page == "advanced_prediction":
        show_advanced_prediction()
    elif current_active_page == "reports":
        show_reports()
    elif current_active_page == "user_management":
        show_user_management()
    elif current_active_page == "kepala_sekolah":
        show_kepala_sekolah()
    elif current_active_page == "guru_mapel":
        show_guru_mapel()
    elif current_active_page == "guru_bk":
        show_guru_bk()
    elif current_active_page == "wali_kelas":
        show_wali_kelas()
    else:
        # Default ke beranda jika halaman tidak dikenali
        show_beranda()

# Jalankan aplikasi jika file di-execute langsung
if __name__ == "__main__":
    main()
