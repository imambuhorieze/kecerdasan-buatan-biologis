# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

# Alias kata → arti yang dimaksud
ALIASES = {
    # Orang
    "jokowi": "Joko Widodo",
    "soeharto": "Suharto",
    "soekarno": "Sukarno",

    # Tempat
    "bali": "Bali (provinsi)",
    "bali indonesia": "Bali (provinsi)",
    "jakarta": "DKI Jakarta",

    # Lain-lain
    "python": "Python (bahasa pemrograman)"
}

def get_alias(kata):
    kata = kata.lower().strip()
    return ALIASES.get(kata, kata)
