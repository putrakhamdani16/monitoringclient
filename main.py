import time
import os
import logging
from system_monitor import collect_data, display_data
from data_manager import TIME_FILE

logging.basicConfig(filename='program.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

if os.path.exists(TIME_FILE):
    os.remove(TIME_FILE)
    logging.info("File uptime_data.json direset saat startup.")

if __name__ == "__main__":
    logging.info("Program dimulai.")
    while True:
        try:
            data = collect_data()
            display_data(data)
            logging.info("Data berhasil diperbarui.")
            print("Menunggu 1 menit untuk pembaruan berikutnya...")
            time.sleep(120)
        except KeyboardInterrupt:
            logging.info("Program dihentikan oleh pengguna.")
            print("Program dihentikan.")
            break
        except Exception as e:
            logging.error(f"Error di loop utama: {e}")
            print(f"Terjadi kesalahan: {e}. Mencoba lagi dalam 10 detik...")
            time.sleep(10)