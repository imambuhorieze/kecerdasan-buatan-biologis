# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import requests
from modules_user import alias

def run(query):
    query = alias.get_alias(query)  # Ambil alias dari modul alias.py

    result = get_summary(query, "id") or get_summary(query, "en")
    if result and not is_irrelevant(result):
        return result

    search_result = search_wiki(query, "id") or search_wiki(query, "en")
    if search_result:
        result = get_summary(search_result, "id") or get_summary(search_result, "en")
        if result and not is_irrelevant(result):
            return result

    return None

def get_summary(title, lang="id"):
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if "extract" in data and data["extract"]:
                return data["extract"]
    except:
        pass
    return None

def search_wiki(query, lang="id"):
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {"action": "query", "list": "search", "srsearch": query, "format": "json"}
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if "query" in data and "search" in data["query"] and data["query"]["search"]:
                return data["query"]["search"][0]["title"]
    except:
        pass
    return None

def is_irrelevant(text):
    kata_tidak_sesuai = ["kapal", "kecelakaan", "tenggelam", "korban", "bencana"]
    return any(kata in text.lower() for kata in kata_tidak_sesuai)
