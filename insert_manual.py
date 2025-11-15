import psycopg2

def insert_users_manual():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='smkn1_sandai',
            user='smkn1_user',
            password='smkn1_password'
        )
        cursor = conn.cursor()
        
        print("🗃️ Memulai insert user ke database smkn1_sandai...")
        
        users = [
            # Admin (should already exist)
            ("admin", "admin123", "admin", "Ahmad Fauzi, S.Kom", None, None, None, "Administrator Sistem", "system"),
            
            # Kepala Sekolah
            ("kepsek", "kepsek123", "kepala_sekolah", "Dr. Surya Adi Wijaya, M.Pd", None, None, None, "Kepala Sekolah", "system"),
            
            # Guru Mapel
            ("siti_math", "guru123", "guru_mapel", "Siti Aisyah, S.Pd", "Matematika", None, "XII TKJ 1, XII TKJ 2, XII MM 1", None, "system"),
            ("budi_bindo", "guru123", "guru_mapel", "Budi Santoso, S.Pd", "Bahasa Indonesia", None, "XII TKJ 1, XII MM 1, XII RPL 1", None, "system"),
            ("dewi_bing", "guru123", "guru_mapel", "Dewi Anggraini, S.Pd", "Bahasa Inggris", None, "XII TKJ 2, XII MM 2, XII RPL 2", None, "system"),
            ("riko_tkj", "guru123", "guru_mapel", "Riko Pratama, S.T", "Teknik Komputer Jaringan", None, "XII TKJ 1, XII TKJ 2", None, "system"),
            ("maya_mm", "guru123", "guru_mapel", "Maya Sari, S.Kom", "Multimedia", None, "XII MM 1, XII MM 2", None, "system"),
            ("hendra_rpl", "guru123", "guru_mapel", "Hendra Setiawan, S.Kom", "Rekayasa Perangkat Lunak", None, "XII RPL 1, XII RPL 2", None, "system"),
            
            # Guru BK
            ("linda_bk", "bk123", "guru_bk", "Linda Wati, S.Psi", None, None, None, "Guru Bimbingan Konseling", "system"),
            
            # Wali Kelas
            ("fajar_tkj1", "wali123", "wali_kelas", "Fajar Nugroho, S.Pd", None, "XII TKJ 1", None, None, "system"),
            ("intan_tkj2", "wali123", "wali_kelas", "Intan Permata, S.Pd", None, "XII TKJ 2", None, None, "system"),
            ("agus_mm1", "wali123", "wali_kelas", "Agus Supriyadi, S.Pd", None, "XII MM 1", None, None, "system"),
            ("nina_mm2", "wali123", "wali_kelas", "Nina Marlina, S.Pd", None, "XII MM 2", None, None, "system"),
            ("dodi_rpl1", "wali123", "wali_kelas", "Dodi Kurniawan, S.Kom", None, "XII RPL 1", None, None, "system"),
            ("sari_rpl2", "wali123", "wali_kelas", "Sari Indah, S.Kom", None, "XII RPL 2", None, None, "system")
        ]
        
        inserted_count = 0
        skipped_count = 0
        
        for user in users:
            try:
                cursor.execute("""
                    INSERT INTO users 
                    (username, password, role, full_name, mata_pelajaran, kelas, kelas_diajar, jabatan, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (username) DO NOTHING
                """, user)
                
                if cursor.rowcount > 0:
                    print(f"✅ INSERTED: {user[0]}")
                    inserted_count += 1
                else:
                    print(f"⚠️ SKIPPED (already exists): {user[0]}")
                    skipped_count += 1
                    
            except Exception as e:
                print(f"❌ ERROR: {user[0]} - {e}")
        
        conn.commit()
        
        # Count total users
        cursor.execute("SELECT COUNT(*) FROM users")
        total_count = cursor.fetchone()[0]
        
        print(f"\n📊 SUMMARY:")
        print(f"✅ Inserted: {inserted_count} users")
        print(f"⚠️ Skipped: {skipped_count} users") 
        print(f"📈 Total in database: {total_count} users")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")

if __name__ == "__main__":
    insert_users_manual()
