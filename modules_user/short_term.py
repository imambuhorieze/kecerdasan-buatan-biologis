# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import time

class ShortTermMemory:
    def __init__(self):
        # key = teks, value = (jawaban, timestamp)
        self.memory = {}
        self.expiry_time = 120  # detik sebelum lupa otomatis

    def remember(self, key, value):
        """Simpan memori pendek"""
        self.memory[key.lower()] = (value, time.time())

    def get(self, key):
        """Ambil memori pendek jika belum kedaluwarsa"""
        item = self.memory.get(key.lower())
        if not item:
            return None
        value, timestamp = item
        if time.time() - timestamp > self.expiry_time:
            del self.memory[key.lower()]
            return None
        return value

    def decay(self):
        """Hapus memori yang sudah kedaluwarsa"""
        now = time.time()
        to_delete = [k for k, (_, ts) in self.memory.items() if now - ts > self.expiry_time]
        for k in to_delete:
            del self.memory[k]

    def clear(self):
        """Hapus semua memori pendek"""
        self.memory = {}
