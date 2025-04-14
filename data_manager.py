import time
import os
import json
import psutil
import logging

# File untuk menyimpan data waktu
TIME_FILE = "uptime_data.json"

def load_or_create_uptime():
    """Memuat data waktu dari file atau membuat baru jika tidak ada."""
    current_time = time.time()
    try:
        if os.path.exists(TIME_FILE):
            with open(TIME_FILE, 'r') as f:
                data = json.load(f)
                return data
        else:
            logging.info("File uptime_data.json tidak ditemukan, membuat baru.")
            return {
                'last_run_time': current_time,
                'last_boot_time': psutil.boot_time()
            }
    except Exception as e:
        logging.error(f"Error di load_or_create_uptime: {e}")
        return {
            'last_run_time': current_time,
            'last_boot_time': psutil.boot_time()
        }

def save_uptime(data):
    """Menyimpan data waktu ke file JSON."""
    try:
        with open(TIME_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        logging.error(f"Error di save_uptime: {e}")