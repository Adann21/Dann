
import psycopg2.extras
from utils.config import app_config
import streamlit as st
from datetime import datetime

class PostgreSQLDatabase:
    def __init__(self):
        self.config = app_config['database']
        self.koneksi = None
        self.connect()
        self.test_connection()
    
    def connect(self):
        """Membuat koneksi ke database PostgreSQL"""
        try:
            self.koneksi = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['name'],
                user=self.config['user'],
                password=self.config['password']
            )
            self._buat_tabel_jika_belum_ada()
            print("✅ Koneksi database berhasil dibuat")
        except Exception as error:
            print(f"❌ Error koneksi database: {error}")
            raise
    
    def test_connection(self):
        """Test koneksi database"""
        try:
            with self.koneksi.cursor() as kursor:
                kursor.execute("SELECT current_database(), current_user, version();")
                db_info = kursor.fetchone()
                db_name, db_user, db_version = db_info
                
                kursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
                table_count = kursor.fetchone()[0]
                
                kursor.execute("SELECT COUNT(*) FROM users")
                user_count = kursor.fetchone()[0]
                
                print("🔍 **DATABASE CONNECTION TEST**")
                print(f"   ✅ Database: {db_name}")
                print(f"   ✅ User: {db_user}")
                print(f"   ✅ PostgreSQL: {db_version.split(',')[0]}")
                print(f"   📊 Tables: {table_count} table(s)")
                print(f"   👥 Users: {user_count} user(s)")
                print("🎉 **KONEKSI DATABASE BERHASIL**")
                
            return True
        except Exception as error:
            print(f"❌ **TEST KONEKSI GAGAL**: {error}")
            return False
    
    def _buat_tabel_jika_belum_ada(self):
        """Membuat tabel-tabel yang diperlukan"""
        try:
            with self.koneksi.cursor() as kursor:
                # Buat tabel users
                kursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        role VARCHAR(20) NOT NULL,
                        full_name VARCHAR(100) NOT NULL,
                        mata_pelajaran VARCHAR(50),
                        kelas VARCHAR(20),
                        kelas_diajar TEXT,
                        jabatan VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_by VARCHAR(50),
                        updated_at TIMESTAMP,
                        updated_by VARCHAR(50)
                    )
                """)
                
                # Insert admin user jika belum ada
                kursor.execute("""
                    INSERT INTO users (username, password, role, full_name, jabatan, created_by) 
                    SELECT 'admin', 'admin123', 'admin', 'Administrator Sistem', 'Administrator', 'system'
                    WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin')
                """)
                
                # Buat tabel students
                kursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id SERIAL PRIMARY KEY,
                        nis VARCHAR(20) UNIQUE NOT NULL,
                        nama VARCHAR(100) NOT NULL,
                        kelas VARCHAR(20) NOT NULL,
                        nilai_matematika NUMERIC(5,2),
                        nilai_bahasa_indonesia NUMERIC(5,2),
                        nilai_bahasa_inggris NUMERIC(5,2),
                        nilai_kejuruan NUMERIC(5,2),
                        kehadiran NUMERIC(5,2),
                        sikap NUMERIC(5,2),
                        kelulusan BOOLEAN,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Buat tabel predictions
                kursor.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        id SERIAL PRIMARY KEY,
                        student_nis VARCHAR(20) REFERENCES students(nis),
                        prediction_result BOOLEAN NOT NULL,
                        confidence NUMERIC(5,4),
                        model_used VARCHAR(50),
                        features_used TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                self.koneksi.commit()
                print("✅ Tabel database siap untuk data real dari sekolah")
                
        except Exception as error:
            self.koneksi.rollback()
            print(f"❌ Error membuat tabel: {error}")
    
    def get_user(self, username):
        """Mengambil data user berdasarkan username"""
        try:
            with self.koneksi.cursor(cursor_factory=psycopg2.extras.DictCursor) as kursor:
                kursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = kursor.fetchone()
                return dict(user) if user else None
        except Exception as error:
            print(f"❌ Error mengambil data user: {error}")
            return None
    
    def get_all_users(self):
        """Mengambil semua data user"""
        try:
            with self.koneksi.cursor(cursor_factory=psycopg2.extras.DictCursor) as kursor:
                kursor.execute("SELECT * FROM users ORDER BY username")
                users = kursor.fetchall()
                return [dict(user) for user in users]
        except Exception as error:
            print(f"❌ Error mengambil data semua user: {error}")
            return []
    
    def add_user(self, user_data):
        """Menambah user baru"""
        try:
            with self.koneksi.cursor() as kursor:
                kursor.execute("""
                    INSERT INTO users 
                    (username, password, role, full_name, mata_pelajaran, kelas, kelas_diajar, jabatan, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_data['username'],
                    user_data['password'],
                    user_data['role'],
                    user_data['full_name'],
                    user_data.get('mata_pelajaran'),
                    user_data.get('kelas'),
                    user_data.get('kelas_diajar'),
                    user_data.get('jabatan'),
                    user_data.get('created_by')
                ))
                self.koneksi.commit()
                return True
        except Exception as error:
            self.koneksi.rollback()
            print(f"❌ Error menambah user: {error}")
            return False
    
    def update_user(self, username, updated_data):
        """Update user data"""
        try:
            with self.koneksi.cursor() as kursor:
                set_clause = []
                values = []
                
                for key, value in updated_data.items():
                    if key != 'username':
                        set_clause.append(f"{key} = %s")
                        values.append(value)
                
                values.append(username)
                
                kursor.execute(f"""
                    UPDATE users 
                    SET {', '.join(set_clause)}, updated_at = CURRENT_TIMESTAMP
                    WHERE username = %s
                """, values)
                
                self.koneksi.commit()
                return kursor.rowcount > 0
                
        except Exception as error:
            self.koneksi.rollback()
            print(f"❌ Error mengupdate user: {error}")
            return False
    
    def delete_user(self, username):
        """Delete user by username"""
        try:
            with self.koneksi.cursor() as kursor:
                kursor.execute("DELETE FROM users WHERE username = %s", (username,))
                self.koneksi.commit()
                return kursor.rowcount > 0
        except Exception as error:
            self.koneksi.rollback()
            print(f"❌ Error menghapus user: {error}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.koneksi:
            self.koneksi.close()

# Buat instance global
print("🔄 Membuat instance database...")
pg_db = PostgreSQLDatabase()
db = pg_db
