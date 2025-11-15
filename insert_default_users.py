from models.database import pg_db

# Data user default
default_users = [
    # Kepala Sekolah
    {
        "username": "kepsek",
        "password": "kepsek123", 
        "role": "kepala_sekolah",
        "full_name": "Dr. Surya Adi Wijaya, M.Pd",
        "jabatan": "Kepala Sekolah",
        "created_by": "system"
    },
    
    # Guru Mata Pelajaran
    {
        "username": "siti_math",
        "password": "guru123",
        "role": "guru_mapel",
        "full_name": "Siti Aisyah, S.Pd",
        "mata_pelajaran": "Matematika",
        "kelas_diajar": "XII TKJ 1, XII TKJ 2, XII MM 1",
        "created_by": "system"
    },
    
    {
        "username": "budi_bindo",
        "password": "guru123",
        "role": "guru_mapel", 
        "full_name": "Budi Santoso, S.Pd",
        "mata_pelajaran": "Bahasa Indonesia",
        "kelas_diajar": "XII TKJ 1, XII MM 1, XII RPL 1",
        "created_by": "system"
    },
    
    {
        "username": "dewi_bing",
        "password": "guru123",
        "role": "guru_mapel",
        "full_name": "Dewi Anggraini, S.Pd",
        "mata_pelajaran": "Bahasa Inggris", 
        "kelas_diajar": "XII TKJ 2, XII MM 2, XII RPL 2",
        "created_by": "system"
    },
    
    {
        "username": "riko_tkj",
        "password": "guru123",
        "role": "guru_mapel",
        "full_name": "Riko Pratama, S.T",
        "mata_pelajaran": "Teknik Komputer Jaringan",
        "kelas_diajar": "XII TKJ 1, XII TKJ 2",
        "created_by": "system"
    },
    
    {
        "username": "maya_mm",
        "password": "guru123", 
        "role": "guru_mapel",
        "full_name": "Maya Sari, S.Kom",
        "mata_pelajaran": "Multimedia",
        "kelas_diajar": "XII MM 1, XII MM 2",
        "created_by": "system"
    },
    
    {
        "username": "hendra_rpl", 
        "password": "guru123",
        "role": "guru_mapel",
        "full_name": "Hendra Setiawan, S.Kom",
        "mata_pelajaran": "Rekayasa Perangkat Lunak",
        "kelas_diajar": "XII RPL 1, XII RPL 2",
        "created_by": "system"
    },
    
    # Guru BK
    {
        "username": "linda_bk",
        "password": "bk123",
        "role": "guru_bk", 
        "full_name": "Linda Wati, S.Psi",
        "jabatan": "Guru Bimbingan Konseling",
        "created_by": "system"
    },
    
    # Wali Kelas
    {
        "username": "fajar_tkj1",
        "password": "wali123",
        "role": "wali_kelas",
        "full_name": "Fajar Nugroho, S.Pd",
        "kelas": "XII TKJ 1",
        "created_by": "system"
    },
    
    {
        "username": "intan_tkj2",
        "password": "wali123",
        "role": "wali_kelas",
        "full_name": "Intan Permata, S.Pd",
        "kelas": "XII TKJ 2", 
        "created_by": "system"
    },
    
    {
        "username": "agus_mm1",
        "password": "wali123",
        "role": "wali_kelas", 
        "full_name": "Agus Supriyadi, S.Pd",
        "kelas": "XII MM 1",
        "created_by": "system"
    },
    
    {
        "username": "nina_mm2",
        "password": "wali123",
        "role": "wali_kelas",
        "full_name": "Nina Marlina, S.Pd", 
        "kelas": "XII MM 2",
        "created_by": "system"
    },
    
    {
        "username": "dodi_rpl1",
        "password": "wali123",
        "role": "wali_kelas",
        "full_name": "Dodi Kurniawan, S.Kom",
        "kelas": "XII RPL 1",
        "created_by": "system"
    },
    
    {
        "username": "sari_rpl2", 
        "password": "wali123",
        "role": "wali_kelas",
        "full_name": "Sari Indah, S.Kom",
        "kelas": "XII RPL 2",
        "created_by": "system"
    }
]

# Insert users
print("Inserting default users...")
for user_data in default_users:
    if not pg_db.get_user(user_data['username']):
        success = pg_db.add_user(user_data)
        if success:
            print(f"✅ Added: {user_data['username']}")
        else:
            print(f"❌ Failed: {user_data['username']}")
    else:
        print(f"⚠️ Already exists: {user_data['username']}")

print("Done!")
