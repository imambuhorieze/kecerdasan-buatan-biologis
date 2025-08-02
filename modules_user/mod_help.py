# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os

FOLDER_AI = "modules_ai"
GUIDE_FILE = os.path.join(FOLDER_AI, "_guides.txt")

def run(core, user_input):
    cmd = user_input.lower().strip()

    # Panduan program spesifik
    if cmd.startswith("cara pakai"):
        program_name = cmd[10:].strip().lower()
        if not os.path.exists(GUIDE_FILE):
            return "⚠ Belum ada panduan program."
        with open(GUIDE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"- {program_name}:"):
                    return f"📘 Panduan {program_name}:\n" + line[len(program_name)+3:].strip()
        return f"⚠ Panduan untuk '{program_name}' tidak ditemukan."

    # Daftar semua panduan
    if cmd == "bantuan":
        if not os.path.exists(GUIDE_FILE):
            return "⚠ Belum ada panduan program."
        with open(GUIDE_FILE, "r", encoding="utf-8") as f:
            guides = f.read().strip()
        return "📋 Daftar Program AI:\n" + guides

    return None
