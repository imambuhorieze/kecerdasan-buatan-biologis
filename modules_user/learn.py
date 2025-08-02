# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os
import json

# Gunakan folder data pusat
DATA_FOLDER = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_FOLDER, exist_ok=True)

DATA_FILE = os.path.join(DATA_FOLDER, "learn_data.json")

# Buat file kosong jika belum ada
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def run(input_data, mode="ask"):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if mode == "ask":
        return data.get(input_data.lower())

    elif mode == "teach":
        pertanyaan, jawaban = input_data
        data[pertanyaan.lower()] = jawaban
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
