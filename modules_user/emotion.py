# Copyright (c) 2025 Imam Buhori
# Licensed for academic research and educational purposes only.
# Commercial use of this code, in whole or in part, is strictly prohibited
# without prior written permission from the copyright holder.
# Contact: imambuhorieze@gmail.com

import random

class EmotionSystem:
    def __init__(self):
        self.moods = ["senang", "netral", "sedih", "marah"]
        self.current_mood = "netral"

    def update_mood(self):
        self.current_mood = random.choice(self.moods)

    def get_mood(self):
        return self.current_mood

    def style_response(self, teks, mood):
        if mood == "senang":
            return teks + " 😊"
        elif mood == "sedih":
            return teks + " 😔"
        elif mood == "marah":
            return teks.upper() + "!!! 😠"
        return teks
