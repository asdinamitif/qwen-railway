import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import requests
import json
import subprocess
import os
import base64
import pyautogui
import pyttsx3
import speech_recognition as sr
import time
from tkinter import filedialog
from io import BytesIO

# --- Константы и настройки ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GIFLabel(ctk.CTkLabel):
    """Кастомный виджет для отображения анимированного GIF"""
    def __init__(self, master, image_path, **kwargs):
        self._frames = []
        try:
            self._gif = Image.open(image_path)
            for i in range(self._gif.n_frames):
                self._gif.seek(i)
                self._frames.append(ctk.CTkImage(self._gif.copy(), size=(150, 150)))
        except Exception as e:
            print(f"Ошибка загрузки GIF: {e}")
            self._frames = [None]

        super().__init__(master, text="", **kwargs)
        if self._frames[0]:
            self._animate(0)

    def _animate(self, idx):
        frame = self._frames[idx]
        self.configure(image=frame)
        self.after(100, self._animate, (idx + 1) % len(self._frames))

class AsyaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("АСЯ — Ультимативный ИИ Ассистент")
        self.geometry("1100x700")

        # Состояние
        self.config = self.load_config()
        self.backend_url = self.config.get("asya_backend_url", "http://localhost:8081/v1")
        self.voice_enabled = True
        self.stt_enabled = False
        self.current_location = "Неизвестно"
        self.attached_image_b64 = None

        # Инициализация голоса
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Layout: Sidebar + Content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="АСЯ", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(pady=20)

        # Маскот (если есть файл)
        if os.path.exists("mascot.gif"):
            self.mascot = GIFLabel(self.sidebar, "mascot.gif")
            self.mascot.pack(pady=10)
        else:
            self.mascot_placeholder = ctk.CTkLabel(self.sidebar, text="[Анимация АСИ]", width=150, height=150, fg_color="gray20")
            self.mascot_placeholder.pack(pady=10)

        self.btn_chat = ctk.CTkButton(self.sidebar, text="Чат", command=lambda: self.show_page("chat"))
        self.btn_chat.pack(pady=10, padx=20)

        self.btn_vpn = ctk.CTkButton(self.sidebar, text="VPN", command=lambda: self.show_page("vpn"))
        self.btn_vpn.pack(pady=10, padx=20)

        self.btn_settings = ctk.CTkButton(self.sidebar, text="Настройки", command=lambda: self.show_page("settings"))
        self.btn_settings.pack(pady=10, padx=20)

        self.location_label = ctk.CTkLabel(self.sidebar, text="Локация: Поиск...", font=ctk.CTkFont(size=10))
        self.location_label.pack(side="bottom", pady=20)

        # --- Content Area ---
        self.pages = {}
        self.create_chat_page()
        self.create_vpn_page()
        self.create_settings_page()

        self.show_page("chat")

        # Запуск фоновых задач
        threading.Thread(target=self.detect_location, daemon=True).start()

    # --- Инициализация страниц ---
    def create_chat_page(self):
        page = ctk.CTkFrame(self, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(0, weight=1)

        self.chat_display = ctk.CTkScrollableFrame(page)
        self.chat_display.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")

        input_frame = ctk.CTkFrame(page, fg_color="transparent")
        input_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.btn_attach = ctk.CTkButton(input_frame, text="+", width=40, command=self.attach_file)
        self.btn_attach.pack(side="left", padx=(0, 10))

        self.btn_screen = ctk.CTkButton(input_frame, text="📸", width=40, command=self.capture_screen)
        self.btn_screen.pack(side="left", padx=(0, 10))

        self.btn_mic = ctk.CTkButton(input_frame, text="🎤", width=40, command=self.toggle_mic)
        self.btn_mic.pack(side="left", padx=(0, 10))

        self.chat_entry = ctk.CTkEntry(input_frame, placeholder_text="Спросите АСЮ о чем угодно...", height=40)
        self.chat_entry.pack(side="left", fill="x", expand=True)
        self.chat_entry.bind("<Return>", lambda e: self.send_chat())

        self.btn_send = ctk.CTkButton(input_frame, text="Отправить", width=100, command=self.send_chat)
        self.btn_send.pack(side="right", padx=(10, 0))

        self.pages["chat"] = page

    def create_vpn_page(self):
        page = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(page, text="Управление VPN", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.vpn_status = ctk.CTkLabel(page, text="Статус: Отключено", text_color="red")
        self.vpn_status.pack(pady=10)

        self.vpn_url_entry = ctk.CTkEntry(page, placeholder_text="URL конфига VPN", width=400)
        self.vpn_url_entry.pack(pady=10)

        ctk.CTkButton(page, text="Подключить VPN", fg_color="green", command=self.toggle_vpn).pack(pady=10)
        self.pages["vpn"] = page

    def create_settings_page(self):
        page = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(page, text="Настройки", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        ctk.CTkLabel(page, text="URL Бэкенда (Railway):").pack(pady=5)
        self.url_setting = ctk.CTkEntry(page, width=400)
        self.url_setting.insert(0, self.backend_url)
        self.url_setting.pack(pady=5)

        self.voice_switch = ctk.CTkSwitch(page, text="Голосовые ответы", command=self.toggle_voice_state)
        self.voice_switch.select()
        self.voice_switch.pack(pady=20)

        ctk.CTkButton(page, text="Сохранить настройки", command=self.save_settings).pack(pady=20)
        self.pages["settings"] = page

    def show_page(self, name):
        for p in self.pages.values():
            p.grid_forget()
        self.pages[name].grid(row=0, column=1, sticky="nsew")

    # --- Логика ассистента ---
    def setup_voice(self):
        voices = self.engine.getProperty('voices')
        for v in voices:
            if "russian" in v.name.lower() or "female" in v.name.lower():
                self.engine.setProperty('voice', v.id)
                break

    def say(self, text):
        if self.voice_enabled:
            def _speak():
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except: pass
            threading.Thread(target=_speak, daemon=True).start()

    def toggle_mic(self):
        if not self.stt_enabled:
            self.stt_enabled = True
            self.btn_mic.configure(fg_color="red")
            threading.Thread(target=self.listen_to_mic, daemon=True).start()
        else:
            self.stt_enabled = False
            self.btn_mic.configure(fg_color=["#3B8ED0", "#1F6AA5"])

    def listen_to_mic(self):
        while self.stt_enabled:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio, language="ru-RU")
                    self.after(0, lambda: self.set_entry_text(text))
                except:
                    pass
            time.sleep(0.5)

    def set_entry_text(self, text):
        self.chat_entry.delete(0, tk.END)
        self.chat_entry.insert(0, text)
        self.send_chat()

    def detect_location(self):
        try:
            r = requests.get("http://ip-api.com/json/", timeout=5)
            data = r.json()
            self.current_location = f"{data.get('city')}, {data.get('country')}"
            self.location_label.configure(text=f"Локация: {self.current_location}")
        except:
            self.location_label.configure(text="Локация: Не определена")

    def attach_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
        if file_path:
            with open(file_path, "rb") as f:
                self.attached_image_b64 = base64.b64encode(f.read()).decode('utf-8')
            self.add_message("Вы", f"[Прикреплен файл: {os.path.basename(file_path)}]", "user")

    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        buffered = BytesIO()
        screenshot.save(buffered, format="JPEG", quality=70)
        self.attached_image_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        self.add_message("Вы", "[Сделан снимок экрана]", "user")

    def add_message(self, sender, text, role):
        color = "#1f538d" if role == "user" else "#333333"
        msg = ctk.CTkLabel(self.chat_display, text=f"{sender}: {text}", wraplength=700,
                           justify="left", fg_color=color, corner_radius=10, padx=15, pady=8)
        msg.pack(anchor="w" if role == "bot" else "e", pady=5, padx=20)
        self.chat_display._parent_canvas.yview_moveto(1.0)

    def send_chat(self):
        prompt = self.chat_entry.get()
        if not prompt and not self.attached_image_b64: return

        if prompt: self.add_message("Вы", prompt, "user")
        self.chat_entry.delete(0, tk.END)

        threading.Thread(target=self.call_asya_api, args=(prompt,)).start()

    def call_asya_api(self, prompt):
        try:
            system_prompt = "Ты — АСЯ, персональный ассистент."
            if os.path.exists("asya_system_prompt.txt"):
                with open("asya_system_prompt.txt", "r", encoding="utf-8") as f:
                    system_prompt = f.read()

            content = []
            if prompt: content.append({"type": "text", "text": prompt})
            if self.attached_image_b64:
                content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.attached_image_b64}"}})
                self.attached_image_b64 = None

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ]

            payload = {
                "model": "qwen",
                "messages": messages,
                "stream": False # Для простоты пока без стриминга в GUI
            }

            resp = requests.post(f"{self.backend_url}/chat/completions", json=payload, timeout=60)
            if resp.status_code == 200:
                answer = resp.json()['choices'][0]['message']['content']
                self.after(0, lambda: self.add_message("АСЯ", answer, "bot"))
                self.say(answer)
            else:
                self.after(0, lambda: self.add_message("АСЯ", f"Ошибка: {resp.text}", "bot"))
        except Exception as e:
            self.after(0, lambda: self.add_message("АСЯ", f"Ошибка связи: {str(e)}", "bot"))

    # --- Остальные функции ---
    def toggle_vpn(self):
        url = self.vpn_url_entry.get()
        self.vpn_status.configure(text="Статус: Подключение...", text_color="orange")

        def _run_vpn():
            try:
                # Попытка использовать системные инструменты в зависимости от ОС
                if os.name == 'nt': # Windows
                    # Пример для WireGuard или OpenVPN если они в PATH
                    # subprocess.run(["wireguard", "/installservice", url], check=True)
                    pass
                else: # Linux/macOS
                    # subprocess.run(["nmcli", "connection", "up", url], check=True)
                    pass

                time.sleep(2)
                self.after(0, lambda: self.vpn_status.configure(text="Статус: Работает (Эмуляция/Системный вызов)", text_color="green"))
            except Exception as e:
                self.after(0, lambda: self.vpn_status.configure(text=f"Ошибка: {str(e)}", text_color="red"))

        threading.Thread(target=_run_vpn, daemon=True).start()

    def toggle_voice_state(self):
        self.voice_enabled = self.voice_switch.get()

    def save_settings(self):
        self.backend_url = self.url_setting.get()
        with open("asya_config.json", "w", encoding="utf-8") as f:
            json.dump({"asya_backend_url": self.backend_url}, f)
        self.show_page("chat")

    def load_config(self):
        if os.path.exists("asya_config.json"):
            with open("asya_config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

if __name__ == "__main__":
    app = AsyaApp()
    app.mainloop()
