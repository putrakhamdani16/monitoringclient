import time
import socket
import psutil
import pytz
from datetime import datetime
import logging
from utils import (get_mac_address, get_serial_number, 
                  get_system_manufacturer, get_system_model, get_bios_version, 
                  get_os_version, get_microsoft_account_username)
from data_manager import load_or_create_uptime, save_uptime

def format_uptime(seconds):
    """Mengonversi detik ke format hari, jam, menit, detik seperti Task Manager."""
    days = int(seconds // (24 * 3600))
    seconds %= (24 * 3600)
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"

def detect_system_state(uptime_data):
    """Mendeteksi apakah sistem dalam keadaan shutdown, sleep, atau aktif."""
    try:
        current_time = time.time()
        current_boot_time = psutil.boot_time()
        last_run_time = uptime_data.get('last_run_time', current_time)
        last_boot_time = uptime_data.get('last_boot_time', current_boot_time)

        time_gap = current_time - last_run_time
        if time_gap > 300:  # Threshold 5 menit untuk Sleep/Shutdown
            if current_boot_time > last_boot_time:
                return "Shutdown", time_gap
            else:
                return "Sleep", time_gap
        return "Active", time_gap
    except Exception as e:
        logging.error(f"Error di detect_system_state: {e}")
        return "Unknown", 0

def collect_data():
    """Mengumpulkan data sistem dan status waktu."""
    try:
        uptime_data = load_or_create_uptime()
        current_time = time.time()
        wib_timezone = pytz.timezone('Asia/Jakarta')

        state, time_gap = detect_system_state(uptime_data)
        data = {}
        data['last_state'] = state
        data['state_duration'] = time_gap

        data['username'] = get_microsoft_account_username()
        data['computer_name'] = socket.gethostname()
        data['ip_address'] = socket.gethostbyname(socket.gethostname())
        data['mac_address'] = get_mac_address()
        data['serial_number'] = get_serial_number()
        data['system_manufacturer'] = get_system_manufacturer()
        data['system_model'] = get_system_model()
        data['bios_version'] = get_bios_version()
        data['os_version'] = get_os_version()

        # Uptime saat ini: berdasarkan waktu sejak boot sistem
        uptime_seconds = current_time - psutil.boot_time()
        data['uptime'] = format_uptime(uptime_seconds)

        uptime_data['last_run_time'] = current_time
        uptime_data['last_boot_time'] = psutil.boot_time()
        save_uptime(uptime_data)

        software_usage = []
        for proc in psutil.process_iter(['name', 'create_time']):
            usage_time = time.time() - proc.info['create_time']
            software_usage.append({'name': proc.info['name'], 'usage_time': int(usage_time)})
        data['software_usage'] = software_usage

        data['timestamp'] = datetime.now(wib_timezone).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + ' WIB'
        data['boot_time'] = datetime.fromtimestamp(psutil.boot_time(), wib_timezone).strftime('%Y-%m-%d %H:%M:%S WIB')

        return data
    except Exception as e:
        logging.error(f"Error di collect_data: {e}")
        return None

def display_data(data):
    """Menampilkan data yang dikumpulkan ke konsol."""
    if data is None:
        print("Gagal mengumpulkan data.")
        return
    print(f"Username: {data['username']}")
    print(f"Nama Komputer: {data['computer_name']}")
    print(f"Alamat IP: {data['ip_address']}")
    print(f"Alamat MAC: {data['mac_address']}")
    print(f"Nomor Seri: {data['serial_number']}")
    print(f"Produsen Sistem: {data['system_manufacturer']}")
    print(f"Model Sistem: {data['system_model']}")
    print(f"Versi BIOS: {data['bios_version']}")
    print(f"Versi OS: {data['os_version']}")
    print(f"Uptime (sejak {data['boot_time']}): {data['uptime']}")
    print(f"Status Terakhir: {data['last_state']} (Durasi: {data['state_duration']:.2f} detik)")
    print("Penggunaan Software:")
    for app in data['software_usage']:
        print(f"  - {app['name']}: {app['usage_time']} detik")
    print(f"Data Diambil Pada: {data['timestamp']}")