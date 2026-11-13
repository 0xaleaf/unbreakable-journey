import os
import winreg

print("=" * 60)
print("     PROGRAM PEMINDAI SELURUH LOKASI INSTALASI APLIKASI     ")
print("=" * 60)

# Kumpulan set untuk menghindari duplikasi nama aplikasi saat cetak hasil
apps_c = set()
apps_d = set()
apps_system = set()

def scan_registry(hive, subkey):
    """Fungsi melacak aplikasi pihak ketiga yang terdaftar di Windows Registry"""
    try:
        with winreg.OpenKey(hive, subkey) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    name, _ = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, name) as sub_key:
                        # Ambil nama aplikasi dan jalur instalasinya
                        app_name, _ = winreg.QueryValueEx(sub_key, "DisplayName")
                        install_path, _ = winreg.QueryValueEx(sub_key, "InstallLocation")
                        
                        if install_path:
                            path_str = str(install_path).upper()
                            if path_str.startswith("D:"):
                                apps_d.add(app_name)
                            elif path_str.startswith("C:"):
                                apps_c.add(app_name)
                except Exception:
                    continue
    except Exception:
        pass

# 1. Jalankan Pemindaian sistem Windows Registry (64-bit dan 32-bit aplikasi)
registry_paths = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
]

for hive, path in registry_paths:
    scan_registry(hive, path)

# 2. Jalankan Pemindaian folder Start Menu (Tempat aplikasi mendaftarkan diri secara fisik)
start_menu_paths = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    r"C:\Users\LENOVO\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
]

for path in start_menu_paths:
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".lnk"):
                    nama = file.replace(".lnk", "")
                    try:
                        # Deteksi lokasi sederhana berdasarkan analisis biner shortcut
                        with open(os.path.join(root, file), "rb") as f:
                            content = f.read().decode('utf-8', errors='ignore').upper()
                            if "D:\\" in content:
                                apps_d.add(nama)
                            elif "C:\\" in content:
                                apps_c.add(nama)
                            else:
                                apps_system.add(nama)
                    except Exception:
                        continue

# 3. Cetak Output Hasil Pemindaian Secara Rapi
print("\n🔴 APLIKASI DI DRIVE C (Berpotensi Memenuhi Ruang):")
print("-" * 60)
for idx, app in enumerate(sorted(apps_c), 1):
    # Menyaring agar nama aplikasi bersih dan tidak menampilkan kode update/patch komputer
    if not any(x in app.lower() for x in ["kb", "update", "redistributable", "driver"]):
        print(f"{idx}. {app}")

print("\n➡️ APLIKASI AMAN DI DRIVE D:")
print("-" * 60)
for idx, app in enumerate(sorted(apps_d), 1):
    print(f"{idx}. {app}")

print("\n⚙️ APLIKASI SISTEM / WINDOWS STORE:")
print("-" * 60)
# Membatasi tampilan agar tidak membanjiri terminal dengan file sistem bawaan Windows
for idx, app in enumerate(list(sorted(apps_system))[:15], 1):
    print(f"{idx}. {app}")
print("...dan beberapa komponen sistem internal lainnya.")

print("\n" + "=" * 60)
print(f"Hasil Analisis: {len(apps_c)} di C | {len(apps_d)} di D")
print("=" * 60)
