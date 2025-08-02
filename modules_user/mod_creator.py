# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os
import re
from modules_user import nlp_super

FOLDER_AI = "modules_ai"
GUIDE_FILE = os.path.join(FOLDER_AI, "_guides.txt")
TEMP_EDIT_FILE = os.path.join(FOLDER_AI, "_temp_edit.txt")  # simpan status edit

def run(core, user_input):
    cmd = user_input.lower()

    # ======== Buat Program ========
    if cmd.startswith("buat program"):
        deskripsi = user_input[13:].strip()
        if not deskripsi:
            return "Harap beri deskripsi program. Contoh: 'buat program kalkulator'."

        nama_modul = re.sub(r'\W+', '_', deskripsi.split()[0].lower())
        file_path = os.path.join(FOLDER_AI, f"{nama_modul}.py")

        if os.path.exists(file_path):
            return f"Program '{nama_modul}' sudah ada."

        kode, panduan = generate_code_with_guide(deskripsi)

        os.makedirs(FOLDER_AI, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(kode)

        save_guide(nama_modul, panduan)
        nlp_super.ajari_kata_kunci(nama_modul, "lokal")

        core.load_all_modules()
        return f"✅ Program '{nama_modul}' berhasil dibuat.\n\n📌 Cara menjalankan:\n{panduan}"

    # ======== Edit Program ========
    if cmd.startswith("edit program"):
        nama_modul = re.sub(r'\W+', '_', user_input[13:].strip().lower())
        file_path = os.path.join(FOLDER_AI, f"{nama_modul}.py")

        if not os.path.exists(file_path):
            return f"❌ Program '{nama_modul}' tidak ditemukan."

        with open(file_path, "r", encoding="utf-8") as f:
            kode = f.read()

        # Simpan status program yang sedang diedit
        with open(TEMP_EDIT_FILE, "w", encoding="utf-8") as f:
            f.write(file_path)

        return f"📂 Mengedit '{nama_modul}'.\nKetik kode baru dan akhiri dengan perintah: simpan program"

    # ======== Simpan Program setelah Edit ========
    if cmd.startswith("simpan program"):
        if not os.path.exists(TEMP_EDIT_FILE):
            return "⚠ Tidak ada program yang sedang diedit."

        with open(TEMP_EDIT_FILE, "r", encoding="utf-8") as f:
            file_path = f.read().strip()

        kode_baru = user_input[15:].strip()
        if not kode_baru:
            return "⚠ Tidak ada kode baru yang diberikan."

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(kode_baru)

        os.remove(TEMP_EDIT_FILE)
        core.load_all_modules()
        return f"💾 Program '{os.path.basename(file_path)[:-3]}' berhasil disimpan."

    # ======== Hapus Program ========
    if cmd.startswith("hapus program"):
        nama_modul = re.sub(r'\W+', '_', user_input[14:].strip().lower())
        file_path = os.path.join(FOLDER_AI, f"{nama_modul}.py")

        if not os.path.exists(file_path):
            return f"❌ Program '{nama_modul}' tidak ditemukan."

        os.remove(file_path)
        remove_guide(nama_modul)
        hapus_kata_kunci_nlp(nama_modul)

        core.load_all_modules()
        return f"🗑 Program '{nama_modul}' berhasil dihapus."

    # ======== Daftar Program ========
    if cmd == "daftar program":
        if not os.path.exists(GUIDE_FILE):
            return "Belum ada program AI yang dibuat."
        with open(GUIDE_FILE, "r", encoding="utf-8") as f:
            return "📋 Daftar Program AI:\n" + f.read()

    return None


def generate_code_with_guide(deskripsi):
    """Generator kode sederhana + panduan"""
    if "kalkulator" in deskripsi.lower():
        kode = """def run(core, user_input):
    if any(op in user_input for op in ['+', '-', '*', '/']):
        try:
            hasil = eval(user_input.replace('x', '*').replace('÷', '/'))
            return f"[Kalkulator] Hasil: {hasil}"
        except Exception as e:
            return f"[Kalkulator] Error: {e}"
    return None
"""
        panduan = "Ketik perhitungan langsung, misalnya: 5 + 3 atau 10 x 4"
        return kode, panduan

    elif "salam" in deskripsi.lower():
        kode = """def run(core, user_input):
    if user_input.lower() in ['halo', 'hai', 'hay', 'hi']:
        return "Halo! Senang bertemu denganmu."
    return None
"""
        panduan = "Ketik 'halo', 'hai', atau 'hay' untuk mendapat balasan salam."
        return kode, panduan

    else:
        kode = f"""def run(core, user_input):
    if '{deskripsi.lower()}' in user_input.lower():
        return "Ini adalah respon otomatis untuk '{deskripsi}'."
    return None
"""
        panduan = f"Ketik kalimat yang mengandung '{deskripsi.lower()}' untuk memicu respon."
        return kode, panduan


def save_guide(program_name, guide):
    """Simpan panduan program ke file"""
    with open(GUIDE_FILE, "a", encoding="utf-8") as f:
        f.write(f"- {program_name}: {guide}\n")


def remove_guide(program_name):
    """Hapus panduan program dari file"""
    if not os.path.exists(GUIDE_FILE):
        return
    with open(GUIDE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(GUIDE_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            if not line.startswith(f"- {program_name}:"):
                f.write(line)


def hapus_kata_kunci_nlp(kata):
    """Hapus kata kunci dari nlp_super"""
    data = nlp_super.load_data()
    kata_lower = kata.lower()
    if kata_lower in data["lokal"]:
        data["lokal"].remove(kata_lower)
    nlp_super.save_data(data)
