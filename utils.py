import uuid
import os
import wmi
import win32api
import win32net
import winreg
import platform
import sys
import logging

# Konfigurasi logging
logging.basicConfig(filename='program.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_mac_address():
    """Mengambil alamat MAC perangkat."""
    try:
        mac = uuid.getnode()
        return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
    except Exception as e:
        logging.error(f"Error di get_mac_address: {e}")
        return "Unknown"

def get_serial_number():
    """Mengambil nomor seri perangkat."""
    try:
        w = wmi.WMI()
        for system in w.Win32_ComputerSystemProduct():
            return system.IdentifyingNumber.strip()
    except Exception as e:
        logging.error(f"Error di get_serial_number: {e}")
        return "Unknown"

def get_system_manufacturer():
    """Mengambil nama produsen sistem."""
    try:
        w = wmi.WMI()
        for system in w.Win32_ComputerSystem():
            return system.Manufacturer.strip()
    except Exception as e:
        logging.error(f"Error di get_system_manufacturer: {e}")
        return "Unknown"

def get_system_model():
    """Mengambil model sistem."""
    try:
        w = wmi.WMI()
        for system in w.Win32_ComputerSystem():
            return system.Model.strip()
    except Exception as e:
        logging.error(f"Error di get_system_model: {e}")
        return "Unknown"

def get_bios_version():
    """Mengambil versi BIOS."""
    try:
        w = wmi.WMI()
        for bios in w.Win32_BIOS():
            return bios.SMBIOSBIOSVersion.strip()
    except Exception as e:
        logging.error(f"Error di get_bios_version: {e}")
        return "Unknown"

def get_os_version():
    """Mengambil versi sistem operasi."""
    try:
        os_name = platform.system()
        if os_name == "Windows":
            win_version = sys.getwindowsversion()
            build_number = win_version.build
            return "Windows 11" if build_number >= 22000 else "Windows 10"
        return os_name + ' ' + platform.release()
    except Exception as e:
        logging.error(f"Error di get_os_version: {e}")
        return "Unknown"

def get_microsoft_account_username():
    """Mengambil username, termasuk akun Microsoft jika tersedia."""
    try:
        username = win32api.GetUserName()
        user_info = win32net.NetUserGetInfo(None, username, 2)
        full_name = user_info.get('full_name', username)
        
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI")
        email = winreg.QueryValueEx(key, "LastLoggedOnUser")[0]
        if email and '@' in email:
            return email
        return full_name if full_name else username
    except Exception as e:
        logging.error(f"Error di get_microsoft_account_username: {e}")
        return os.getlogin()