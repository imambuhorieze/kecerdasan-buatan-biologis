# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os
import re

FOLDER_AI = "modules_ai"
FOLDER_USER = "modules_user"

def run(core, user_input):
    cmd = user_input.lower()

    # Buat modul
    if cmd.startswith("buat modul ai"):
        return buat_modul(FOLDER_AI, user_input[13:].strip(), core)
    elif cmd.startswith("buat modul saya"):
        return buat_modul(FOLDER_USER, user_input[15:].strip(), core)

    # Hapus modul
    if cmd.startswith("hapus modul ai"):
        return hapus_modul(FOLDER_AI, user_input[14:].strip(), core)
    elif cmd.startswith("hapus modul saya"):
        return hapus_modul(FOLDER_USER, user_input[16:].strip(), core)

    return None

def buat_modul(folder, deskripsi, core):
    if not deskripsi:
        return "Harap beri deskripsi modul."

    nama_modul = re.sub(r'\W+', '_', deskripsi.split()[0].lower())
    file_path = os.path.join(folder, f"{nama_modul}.py")

    if os.path.exists(file_path):
        return f"Modul '{nama_modul}' sudah ada."

    kode = generate_module_code(deskripsi)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(kode)

    core.load_all_modules()
    return f"Modul '{nama_modul}' berhasil dibuat di {folder}."

def hapus_modul(folder, nama_modul, core):
    nama_modul = re.sub(r'\W+', '_', nama_modul.lower())
    file_path = os.path.join(folder, f"{nama_modul}.py")

    if not os.path.exists(file_path):
        return f"Modul '{nama_modul}' tidak ditemukan di {folder}."

    os.remove(file_path)
    core.load_all_modules()
    return f"Modul '{nama_modul}' berhasil dihapus dari {folder}."

def generate_module_code(deskripsi):
    if "kalkulator" in deskripsi.lower():
        return """def run(core, user_input):
    if any(op in user_input for op in ['+', '-', '*', '/']):
        try:
            hasil = eval(user_input.replace('x', '*').replace('÷', '/'))
            return f"[Kalkulator] Hasil: {hasil}"
        except Exception as e:
            return f"[Kalkulator] Error: {e}"
    return None
"""
    return f"""def run(core, user_input):
    if '{deskripsi.lower()}' in user_input.lower():
        return "Respon otomatis untuk '{deskripsi}'."
    return None
"""
