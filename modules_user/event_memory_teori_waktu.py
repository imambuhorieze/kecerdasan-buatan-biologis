# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os
import json
from datetime import datetime

# Folder khusus untuk data
DATA_FOLDER = "data"
IMPORTANT_FILE = os.path.join(DATA_FOLDER, "events_important.json")
TEMP_FILE = os.path.join(DATA_FOLDER, "events_temp.json")

# Pastikan folder data ada
os.makedirs(DATA_FOLDER, exist_ok=True)

# Pastikan file data ada
for file_path in [IMPORTANT_FILE, TEMP_FILE]:
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

def simpan_peristiwa(pertanyaan, core, penting=False):
    """Simpan peristiwa ke file"""
    file_path = IMPORTANT_FILE if penting else TEMP_FILE

    with open(file_path, "r") as f:
        data = json.load(f)

    data.append({
        "waktu": datetime.now().isoformat(),
        "pertanyaan": pertanyaan,
        "waktu_biologis": core.biological_time
    })

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def muat_peristiwa(penting=False):
    """Muat peristiwa dari file"""
    file_path = IMPORTANT_FILE if penting else TEMP_FILE
    with open(file_path, "r") as f:
        return json.load(f)
