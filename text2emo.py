from transformers import pipeline
import tkinter as tk
from tkinter import messagebox
import random
import time
import json
import threading
import os

try:
    import pyttsx3
    tts_engine = pyttsx3.init()
except ImportError:
    tts_engine = None

# Load Hugging Face emotion classification pipeline
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# Emoji mapping for emotions
emotion_data = {
    "joy": "😄",
    "sadness": "😢",
    "anger": "😠",
    "fear": "😨",
    "love": "😍",
    "surprise": "😲",
    "neutral": "😐"
}

HISTORY_FILE = "emotion_history.json"
GAME_TIME_LIMIT = 30  # seconds


def detect_emotion_ai(text):
    try:
        results = emotion_classifier(text)
        if isinstance(results, list) and isinstance(results[0], list):
            label = results[0][0]['label'].lower()
        elif isinstance(results, list) and isinstance(results[0], dict):
            label = results[0]['label'].lower()
        else:
            label = "neutral"
        return label
    except Exception as e:
        print(f"[Error] {e}")
        return "neutral"


class EmotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Based Text to Emotion Detector")
        self.root.geometry("420x600")
        self.root.configure(bg="#FFA500")
        self.history = self.load_history()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter your text:", font=("Helvetica", 16, "bold"), bg="#FFA500").pack(pady=10)

        self.text_entry = tk.Text(self.root, height=3, font=("Helvetica", 14))
        self.text_entry.pack(pady=10)

        tk.Button(self.root, text="Detect Emotion", font=("Helvetica", 12, "bold"), command=self.detect_emotion_action,
                  bg="lightyellow").pack(pady=5)

        tk.Button(self.root, text="Speak", font=("Helvetica", 12, "bold"), command=self.speak_text,
                  bg="lightyellow").pack(pady=5)

        self.emoji_label = tk.Label(self.root, text="", font=("Helvetica", 64), bg="#FFA500")
        self.emoji_label.pack(pady=20)

        self.result_label = tk.Label(self.root, text="Emotion: ", font=("Helvetica", 18, "bold"), bg="#FFA500")
        self.result_label.pack(pady=10)

        tk.Button(self.root, text="Play Game Mode", font=("Helvetica", 14, "bold"), command=self.start_game,
                  bg="white").pack(pady=10)

        tk.Button(self.root, text="View History", font=("Helvetica", 12, "bold"), command=self.show_history,
                  bg="lightgreen").pack(pady=5)

        tk.Button(self.root, text="Clear History", font=("Helvetica", 12, "bold"), command=self.clear_history,
                  bg="red", fg="white").pack(pady=5)

    def detect_emotion_action(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return
        emotion = detect_emotion_ai(text)
        emoji = emotion_data.get(emotion, "😐")
        self.emoji_label.config(text=emoji)
        self.result_label.config(text=f"Emotion: {emotion.capitalize()}")
        self.save_history(text, emotion)

    def speak_text(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if tts_engine and text:
            tts_engine.say(text)
            tts_engine.runAndWait()

    def start_game(self):
        self.original_word, self.shuffled = self.get_shuffled_word()
        self.remaining_time = GAME_TIME_LIMIT

        game_win = tk.Toplevel(self.root)
        game_win.title("Emotion Word Shuffle Game")
        game_win.geometry("350x320")
        game_win.configure(bg="#FFF8DC")
        self.game_win = game_win

        tk.Label(game_win, text="Unscramble the emotion word:", font=("Helvetica", 14), bg="#FFF8DC").pack(pady=10)
        tk.Label(game_win, text=self.shuffled.upper(), font=("Helvetica", 32, "bold"), bg="#FFF8DC", fg="blue").pack(pady=10)

        self.user_guess_entry = tk.Entry(game_win, font=("Helvetica", 14))
        self.user_guess_entry.pack(pady=5)

        self.timer_label = tk.Label(game_win, text="", font=("Helvetica", 14, "bold"), bg="#FFF8DC")
        self.timer_label.pack(pady=5)

        self.feedback_label = tk.Label(game_win, text="", font=("Helvetica", 14), bg="#FFF8DC")
        self.feedback_label.pack(pady=10)

        tk.Button(game_win, text="Submit", font=("Helvetica", 12), command=self.check_guess).pack(pady=5)

        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_label.config(text=f"Time Left: {self.remaining_time}s")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.feedback_label.config(text="Time's up! Try again.", fg="red")

    def get_shuffled_word(self):
        word = random.choice(list(emotion_data.keys()))
        shuffled = ''.join(random.sample(word, len(word)))
        return word, shuffled

    def check_guess(self):
        guess = self.user_guess_entry.get().strip().lower()
        if guess == self.original_word:
            emoji = emotion_data.get(guess, "😐")
            self.feedback_label.config(text=f"Correct! {emoji} ({guess.capitalize()})", fg="green")
        else:
            self.feedback_label.config(text="Try Again!", fg="red")

    def save_history(self, text, emotion):
        self.history.append({"text": text, "emotion": emotion})
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.history, f, indent=2)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        return []

    def show_history(self):
        history_win = tk.Toplevel(self.root)
        history_win.title("Emotion Detection History")
        history_win.geometry("350x300")
        history_win.configure(bg="#FFFFF0")
        tk.Label(history_win, text="Emotion History", font=("Helvetica", 16, "bold"), bg="#FFFFF0").pack(pady=10)

        text_widget = tk.Text(history_win, font=("Helvetica", 12), wrap="word")
        text_widget.pack(expand=True, fill="both")
        for entry in self.history[-10:]:
            text_widget.insert(tk.END, f"Text: {entry['text']}\nEmotion: {entry['emotion'].capitalize()}\n\n")
        text_widget.config(state="disabled")

    def clear_history(self):
        self.history = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        messagebox.showinfo("History Cleared", "Emotion detection history has been cleared successfully.")


if __name__ == '__main__':
    root = tk.Tk()
    app = EmotionApp(root)
    root.mainloop()
