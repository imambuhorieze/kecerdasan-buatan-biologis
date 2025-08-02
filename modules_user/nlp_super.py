# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os
import json

DATA_FOLDER = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_FOLDER, exist_ok=True)

DATA_FILE = os.path.join(DATA_FOLDER, "nlp_data.json")

DEFAULT_DATA = {
    "lokal": [
        "siapa kamu", "kamu siapa", "nama kamu", "halo", "hai", "hay",
        "assalamualaikum", "selamat pagi", "selamat siang", "selamat sore",
        "selamat malam", "apakabar", "apa kabar", "terima kasih", "makasih",
        "kalkulator", "catat", "lihat peristiwa"
    ],
    "publik": [
        "siapa presiden", "dimana", "kapan", "berapa", "apa itu",
        "pengertian", "definisi", "sejarah", "biografi", "geografi"
    ]
}

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_DATA, f, indent=2)

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def deteksi_jenis_pertanyaan(teks):
    data = load_data()
    teks_lower = teks.strip().lower()

    # Cek kata kunci lokal
    if any(k in teks_lower for k in data["lokal"]):
        return "lokal"

    # Cek kata kunci publik
    if any(k in teks_lower for k in data["publik"]):
        return "publik"

    # Kata tanya → publik
    kata_tanya = ["siapa", "apa", "dimana", "kapan", "berapa", "mengapa", "kenapa", "bagaimana"]
    for kata in kata_tanya:
        if teks_lower.startswith(kata):
            return "publik"

    # Default lokal
    return "lokal"

def ajari_kata_kunci(teks, tipe):
    data = load_data()
    teks_lower = teks.strip().lower()
    if tipe not in ["lokal", "publik"]:
        return
    if teks_lower not in data[tipe]:
        data[tipe].append(teks_lower)
    save_data(data)
