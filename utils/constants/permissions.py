ROLE_PERMISSIONS = {
    "admin": {
        "dashboard": True,
        "user_management": True,
        "data_upload": True,
        "prediction": True,
        "reports": True,
        "settings": True
    },
    "kepala_sekolah": {
        "dashboard": True,
        "user_management": False,
        "data_upload": False,
        "prediction": True,
        "reports": True,
        "settings": False
    },
    "wali_kelas": {
        "dashboard": True,
        "user_management": False,
        "data_upload": True,
        "prediction": True,
        "reports": True,
        "settings": False
    },
    "guru_bk": {
        "dashboard": True,
        "user_management": False,
        "data_upload": True,
        "prediction": True,
        "reports": True,
        "settings": False
    },
    "guru_mapel": {
        "dashboard": True,
        "user_management": False,
        "data_upload": False,
        "prediction": False,
        "reports": True,
        "settings": False
    }
}
