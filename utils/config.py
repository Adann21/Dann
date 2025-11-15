import yaml
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    """
    Memuat konfigurasi dari file YAML dan environment variables
    Environment variables akan override nilai dari YAML
    """
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        # Fallback ke config default jika file tidak ditemukan
        config = get_default_config()
    
    # Override database config dengan environment variables
    database_config = config.get('database', {})
    
    if os.getenv('DB_NAME'):
        database_config['name'] = os.getenv('DB_NAME')
    if os.getenv('DB_USER'):
        database_config['user'] = os.getenv('DB_USER')
    if os.getenv('DB_PASSWORD'):
        database_config['password'] = os.getenv('DB_PASSWORD')
    if os.getenv('DB_HOST'):
        database_config['host'] = os.getenv('DB_HOST')
    if os.getenv('DB_PORT'):
        database_config['port'] = int(os.getenv('DB_PORT'))
    
    config['database'] = database_config
    
    return config

def get_default_config():
    """Config default jika config.yaml tidak ditemukan"""
    return {
        'app': {
            'name': 'Sistem Prediksi Kelulusan SMKN 1 Sandai',
            'version': '2.0.0',
            'debug': True
        },
        'database': {
            'type': 'postgresql',
            'host': 'localhost',
            'port': 5432,
            'name': 'prediksi_kelulusan',
            'user': 'postgres',
            'password': '232102582',
            'file_path': 'data/users.json'
        },
        'model': {
            'algorithm': 'PSO_RandomForest',
            'features': [
                'nilai_matematika',
                'nilai_bahasa_indonesia', 
                'nilai_bahasa_inggris',
                'nilai_kejuruan',
                'kehadiran',
                'sikap'
            ],
            'target': 'kelulusan'
        },
        'roles': {
            'admin': ['read', 'write', 'delete', 'manage_users'],
            'kepala_sekolah': ['read', 'export'],
            'wali_kelas': ['read', 'write'],
            'guru_bk': ['read', 'write'],
            'guru_mapel': ['read']
        }
    }

def get_env_variable(key, default=None):
    """Mengambil environment variable dengan fallback default"""
    return os.getenv(key, default)

# Config instance
app_config = load_config()
secret_key = get_env_variable('APP_SECRET_KEY', 'default-secret-key')
admin_password = get_env_variable('ADMIN_DEFAULT_PASSWORD', 'admin123')

# Test function untuk debug
def print_config():
    """Print konfigurasi untuk debugging"""
    print("=== CONFIGURATION ===")
    print(f"App: {app_config['app']['name']} v{app_config['app']['version']}")
    print(f"Database: {app_config['database']['name']} on {app_config['database']['host']}:{app_config['database']['port']}")
    print(f"User: {app_config['database']['user']}")
    print("=====================")

# Otomatis print config jika di-run langsung
if __name__ == "__main__":
    print_config()