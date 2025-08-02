# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os
import importlib
import inspect

class MimiCoreBiologis:
    def __init__(self):
        self.modules = {}
        self.short_term_memory = None
        self.mood_system = None
        self.load_all_modules()

        # Inisialisasi mood system jika modul emotion tersedia
        if "emotion" in self.modules and hasattr(self.modules["emotion"], "EmotionSystem"):
            try:
                self.mood_system = self.modules["emotion"].EmotionSystem()
                print("[INFO] Mood system berhasil diinisialisasi.")
            except Exception as e:
                print(f"[WARNING] Gagal inisialisasi mood system: {e}")

    def load_all_modules(self):
        """Muat semua modul dari modules_user dan modules_ai"""
        self.modules.clear()
        for folder in ["modules_user", "modules_ai"]:
            if not os.path.exists(folder):
                os.makedirs(folder)
            for file in os.listdir(folder):
                if file.endswith(".py") and not file.startswith("__"):
                    mod_name = file[:-3]
                    try:
                        self.modules[mod_name] = importlib.import_module(f"{folder}.{mod_name}")
                    except Exception as e:
                        print(f"[ERROR] Gagal memuat modul {mod_name}: {e}")

    def process_input(self, user_input):
        teks_lower = user_input.lower().strip()

        # 📌 Daftar modul prioritas (jalankan lebih dulu)
        PRIORITY_MODULES = ["mod_github", "mod_gitclone", "mod_create", "mod_help"]

        # 1️⃣ Jalankan modul prioritas dulu
        for nama_modul in PRIORITY_MODULES:
            if nama_modul in self.modules and hasattr(self.modules[nama_modul], "run"):
                try:
                    sig = inspect.signature(self.modules[nama_modul].run)
                    param_count = len(sig.parameters)
                    hasil = (
                        self.modules[nama_modul].run(user_input)
                        if param_count == 1
                        else self.modules[nama_modul].run(self, user_input)
                    )
                    if hasil:
                        return hasil
                except Exception as e:
                    if "self_repair" in self.modules:
                        self.modules["self_repair"].log_error(nama_modul, str(e))

        # 2️⃣ Jalankan modul lokal tool (kecuali web_search, nlp_super, learn)
        for nama_modul, modul in self.modules.items():
            if nama_modul in PRIORITY_MODULES:
                continue
            if nama_modul not in ["web_search", "nlp_super", "learn"] and hasattr(modul, "run"):
                try:
                    sig = inspect.signature(modul.run)
                    param_count = len(sig.parameters)
                    hasil = modul.run(user_input) if param_count == 1 else modul.run(self, user_input)
                    if hasil:
                        return hasil
                except Exception as e:
                    if "self_repair" in self.modules:
                        self.modules["self_repair"].log_error(nama_modul, str(e))

        # 3️⃣ Cek memori pendek
        if self.short_term_memory:
            jawaban_pendek = self.short_term_memory.get(user_input)
            if jawaban_pendek:
                return f"[Memori Pendek] {jawaban_pendek}"

        # 4️⃣ Cek memori panjang (lokal)
        if "learn" in self.modules:
            jawaban_lokal = self.modules["learn"].run(user_input, mode="ask")
            if jawaban_lokal:
                return f"[Lokal] {jawaban_lokal}"

        # 5️⃣ Gunakan NLP Super untuk memutuskan publik/lokal
        if "nlp_super" in self.modules:
            jenis = self.modules["nlp_super"].deteksi_jenis_pertanyaan(user_input)

            if jenis == "publik" and "web_search" in self.modules:
                jawaban_web = self.modules["web_search"].run(user_input)
                if jawaban_web:
                    if "learn" in self.modules:
                        self.modules["learn"].run((user_input, jawaban_web), mode="teach")
                    return f"[Publik] {jawaban_web}"
                return self.ajarkan(user_input, "publik")

            elif jenis == "lokal":
                return self.ajarkan(user_input, "lokal")

        # 6️⃣ Default → lokal
        return self.ajarkan(user_input, "lokal")

    def ajarkan(self, pertanyaan, tipe_default):
        """Ajarkan jawaban baru"""
        if tipe_default == "lokal":
            new_answer = input("Mimi: Apa jawabannya?\nKamu: ")
            if "learn" in self.modules:
                self.modules["learn"].run((pertanyaan, new_answer), mode="teach")
            return "[Belajar] Terima kasih, aku sudah belajar. 😊"
        else:
            if "web_search" in self.modules:
                jawaban_web = self.modules["web_search"].run(pertanyaan)
                if jawaban_web:
                    if "learn" in self.modules:
                        self.modules["learn"].run((pertanyaan, jawaban_web), mode="teach")
                    return f"[Publik] {jawaban_web}"
            return "Maaf, aku tidak menemukan jawabannya di internet."

    def decay_short_term(self):
        """Kurangi kekuatan memori jangka pendek secara bertahap"""
        if self.short_term_memory:
            self.short_term_memory.decay()
