# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os
import json
import re
import importlib

ERROR_LOG = os.path.join("data", "error_log.json")

# ===========================
# Fungsi untuk mencatat error
# ===========================
def log_error(module_name, error_message):
    os.makedirs("data", exist_ok=True)
    log_data = []
    if os.path.exists(ERROR_LOG):
        try:
            with open(ERROR_LOG, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except:
            log_data = []
    log_data.append({"module": module_name, "error": error_message})
    with open(ERROR_LOG, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

# ===========================
# Jalankan perintah self-repair
# ===========================
def run(core, user_input):
    if user_input.lower() == "perbaiki diri":
        return repair_all_modules(core)
    return None

# ===========================
# Perbaiki semua modul error
# ===========================
def repair_all_modules(core):
    if not os.path.exists(ERROR_LOG):
        return "✅ Tidak ada error yang perlu diperbaiki."

    with open(ERROR_LOG, "r", encoding="utf-8") as f:
        errors = json.load(f)

    perbaikan = []
    for err in errors:
        module_name = err["module"]
        error_msg = err["error"]

        # Perbaiki file Python
        for folder in ["modules_ai", "modules_user"]:
            file_path = os.path.join(folder, f"{module_name}.py")
            if os.path.exists(file_path):
                if fix_python_module(file_path, error_msg):
                    perbaikan.append(f"🛠 {module_name} diperbaiki.")
                else:
                    perbaikan.append(f"⚠ {module_name} tidak bisa diperbaiki otomatis.")

        # Perbaiki file JSON
        for folder in ["data"]:
            file_path = os.path.join(folder, f"{module_name}.json")
            if os.path.exists(file_path):
                if fix_json_file(file_path):
                    perbaikan.append(f"🛠 {module_name}.json diperbaiki.")

    # Bersihkan log setelah perbaikan
    os.remove(ERROR_LOG)
    core.load_all_modules()
    return "\n".join(perbaikan)

# ===========================
# Perbaikan file Python pintar
# ===========================
def fix_python_module(file_path, error_msg):
    fixed = False
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Perbaiki import lama
    if "from modules import" in content:
        content = content.replace("from modules import", "from modules_user import")
        fixed = True

    # 2. Tambahkan fungsi run jika hilang
    if "def run(" not in content:
        content += "\n\ndef run(core, user_input):\n    return None\n"
        fixed = True

    # 3. Perbaiki IndentationError
    if "IndentationError" in error_msg:
        content = re.sub(r"\t", "    ", content)
        fixed = True

    # 4. Perbaiki NameError umum
    match = re.search(r"NameError: name '(\w+)' is not defined", error_msg)
    if match:
        var_name = match.group(1)
        content = f"{var_name} = None\n" + content
        fixed = True

    if fixed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    return fixed

# ===========================
# Perbaikan file JSON
# ===========================
def fix_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json.load(f)
        return False  # JSON sudah valid
    except json.JSONDecodeError:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("{}")  # reset jadi kosong
        return True
