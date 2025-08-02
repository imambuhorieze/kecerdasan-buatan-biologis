# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import os
import subprocess
import sys
import shutil

DOWNLOAD_FOLDER = "github_downloads"

def run(core, user_input):
    cmd = user_input.strip().lower()

    # Perintah install git
    if cmd == "install git":
        return install_git()

    # Perintah clone repo
    if cmd.startswith("gitclone "):
        repo_url = user_input.split(" ", 1)[1].strip()
        if not repo_url:
            return "⚠ Format: gitclone <url_repo>"
        return clone_repo(repo_url)

    return None


def install_git():
    """Install Git di Windows"""
    if shutil.which("git"):
        return "✅ Git sudah terpasang di sistem."

    if os.name == "nt":  # Windows
        try:
            print("[INFO] Mengunduh installer Git...")
            subprocess.run([
                "powershell", 
                "-Command", 
                "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/latest/download/Git-2.43.0-64-bit.exe -OutFile git_installer.exe"
            ], check=True)

            print("[INFO] Menjalankan installer Git...")
            subprocess.run(["git_installer.exe", "/VERYSILENT", "/NORESTART"], check=True)
            os.remove("git_installer.exe")
            return "✅ Git berhasil di-install. Silakan restart CMD/terminal."
        except Exception as e:
            return f"❌ Gagal install Git: {e}"
    else:
        return "⚠ Install Git manual: https://git-scm.com/downloads"


def clone_repo(url):
    """Clone repo ke folder github_downloads"""
    if not shutil.which("git"):
        return "⚠ Git belum terpasang. Jalankan: install git"

    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    try:
        subprocess.run(["git", "clone", url], cwd=DOWNLOAD_FOLDER, check=True)
        return f"✅ Repo berhasil di-clone ke folder '{DOWNLOAD_FOLDER}'."
    except subprocess.CalledProcessError as e:
        return f"❌ Gagal clone repo: {e}"
