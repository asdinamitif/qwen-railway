import tkinter as tk
import customtkinter as ctk
import threading
import requests
import json
import subprocess
import os
import sys

# Настройки GUI
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AsyaGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("АСЯ — Ваш персональный ИИ")
        self.geometry("800x600")

        # Загрузка конфига
        self.config = self.load_config()
        self.backend_url = self.config.get("asya_backend_url", "http://localhost:8081/v1")

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Chat Area
        self.chat_frame = ctk.CTkScrollableFrame(self, width=780, height=450)
        self.chat_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Input Area
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Напишите АСЕ...", width=600)
        self.entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = ctk.CTkButton(self.input_frame, text="Отправить", command=self.send_message)
        self.send_button.pack(side="right", padx=5, pady=5)

        self.add_message("АСЯ", "Привет! Я готова помогать. О чем хочешь поговорить?", "bot")

    def load_config(self):
        try:
            with open("asya_config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def add_message(self, sender, text, role):
        color = "#1f538d" if role == "user" else "#333333"
        msg_label = ctk.CTkLabel(self.chat_frame, text=f"[{sender}]: {text}",
                                 wraplength=700, justify="left", fg_color=color,
                                 corner_radius=10, padx=10, pady=5)
        msg_label.pack(anchor="w" if role == "bot" else "e", pady=5, padx=10)
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def send_message(self):
        user_text = self.entry.get()
        if not user_text: return

        self.add_message("Вы", user_text, "user")
        self.entry.delete(0, tk.END)

        # Поток для запроса к ИИ
        threading.Thread(target=self.get_ai_response, args=(user_text,)).start()

    def get_ai_response(self, text):
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "qwen",
                "messages": [{"role": "user", "content": text}],
                "temperature": 0.7
            }

            response = requests.post(f"{self.backend_url}/chat/completions",
                                     headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                ai_text = result['choices'][0]['message']['content']
                self.after(0, lambda: self.handle_commands(ai_text))
            else:
                self.after(0, lambda: self.add_message("АСЯ", f"Ошибка сервера: {response.status_code}", "bot"))
        except Exception as e:
            self.after(0, lambda: self.add_message("АСЯ", f"Ошибка связи: {str(e)}", "bot"))

    def handle_commands(self, text):
        # Простая логика выполнения команд, если ИИ выдал код
        self.add_message("АСЯ", text, "bot")

        # Если в ответе есть маркеры команд (упрощенно)
        if "```bash" in text:
            # Тут можно добавить логику подтверждения выполнения кода
            pass

if __name__ == "__main__":
    app = AsyaGUI()
    app.mainloop()
