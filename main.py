# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

from mimi_core_biologis import MimiCoreBiologis

if __name__ == "__main__":
    mimi = MimiCoreBiologis()
    print("=== Mimi AI Biologis ===")
    print("Ketik 'exit' untuk keluar.")

    while True:
        user_input = input("\nKamu: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Mimi: Sampai jumpa!")
            break

        # Proses input dan tampilkan jawaban
        jawaban = mimi.process_input(user_input)

        # Mood mempengaruhi gaya bicara
        mimi.mood_system.update_mood()
        jawaban = mimi.mood_system.style_response(jawaban, mimi.mood_system.get_mood())

        print("Mimi:", jawaban)

        # Decay memori pendek secara periodik
        mimi.decay_short_term()
