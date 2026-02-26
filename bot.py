import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import webbrowser  
from javascript import require, On

mineflayer = require('mineflayer')

# Цветовая палитра
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#3d3d3d"
BTN_START = "#28a745"
BTN_STOP = "#dc3545"
TEXT_COLOR = "#e0e0e0"
LINK_COLOR = "#3498db" 


class BotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Stress Tester")
        self.root.geometry("450x580")  
        self.root.configure(bg=BG_COLOR)
        self.is_running = False

        # Заголовок
        tk.Label(root, text="BOT CONTROLLER", font=("Segoe UI", 16, "bold"),
                 bg=BG_COLOR, fg=FG_COLOR).pack(pady=15)

        # --- Контейнер для полей ---
        input_frame = tk.Frame(root, bg=BG_COLOR)
        input_frame.pack(padx=20, fill="x")

        self.create_label_entry(input_frame, "Адрес сервера (IP:PORT):", "entry_address", "myserver.aternos.me:25565")
        self.create_label_entry(input_frame, "Версия игры (напр. 1.21.1):", "entry_version", "1.21.1")
        self.create_label_entry(input_frame, "Никнейм (префикс):", "entry_nick", "MasterDDos")
        self.create_label_entry(input_frame, "Текст сообщения:", "entry_msg", "Это стресс тест, бич!")

        # Чекбокс
        self.var_random = tk.BooleanVar(value=True)
        self.cb_random = tk.Checkbutton(
            root, text="Рандомизировать ник", variable=self.var_random,
            bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR,
            activebackground=BG_COLOR, activeforeground=FG_COLOR,
            font=("Segoe UI", 10)
        )
        self.cb_random.pack(pady=5)

        # Кнопка запуска
        self.btn_start = tk.Button(
            root, text="START TEST", command=self.toggle_test,
            bg=BTN_START, fg=FG_COLOR, font=("Segoe UI", 12, "bold"),
            relief="flat", width=20, height=2, cursor="hand2"
        )
        self.btn_start.pack(pady=15)

        # Статус
        self.status_label = tk.Label(root, text="STATUS: READY", font=("Consolas", 10),
                                     bg=BG_COLOR, fg="#888888")
        self.status_label.pack(pady=5)


        footer_frame = tk.Frame(root, bg=BG_COLOR)
        footer_frame.pack(side="bottom", pady=15)

        tk.Label(footer_frame, text="Бот от dobrozor", font=("Segoe UI", 9),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left")

        link = tk.Label(footer_frame, text="(github)", font=("Segoe UI", 9, "underline"),
                        bg=BG_COLOR, fg=LINK_COLOR, cursor="hand2")
        link.pack(side="left", padx=5)
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://dobrozor.github.io/"))

    def create_label_entry(self, parent, label_text, attr_name, default_val):
        tk.Label(parent, text=label_text, bg=BG_COLOR, fg=TEXT_COLOR,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=40)

        entry = tk.Entry(parent, bg=ACCENT_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR,
                         relief="flat", font=("Segoe UI", 10), width=35)
        entry.insert(0, default_val)
        entry.pack(pady=(0, 10), ipady=5)
        setattr(self, attr_name, entry)

    def create_bot(self, host, port, nick, message, version):
        final_nick = f"{nick}_{random.randint(100, 999)}" if self.var_random.get() else nick
        try:
            bot = mineflayer.createBot({
                'host': host,
                'port': int(port),
                'username': final_nick,
                'version': version
            })

            @On(bot, 'spawn')
            def handle_spawn(*args):
                time.sleep(0.5)
                bot.chat(message)
                time.sleep(0.5)
                bot.quit()

            @On(bot, 'error')
            def handle_error(this, err, *args):
                pass
        except Exception as e:
            print(f"Error: {e}")

    def test_loop(self):
        address = self.entry_address.get()
        nick = self.entry_nick.get()
        message = self.entry_msg.get()
        version = self.entry_version.get()

        if ":" not in address:
            messagebox.showerror("Ошибка", "Используйте формат IP:PORT")
            self.stop_test()
            return

        try:
            host, port = address.split(":")
            while self.is_running:
                self.create_bot(host, port, nick, message, version)
                time.sleep(1)
        except Exception:
            self.stop_test()

    def toggle_test(self):
        if not self.is_running:
            self.is_running = True
            self.btn_start.config(text="STOP TEST", bg=BTN_STOP)
            self.status_label.config(text="STATUS: RUNNING...", fg=BTN_START)
            threading.Thread(target=self.test_loop, daemon=True).start()
        else:
            self.stop_test()

    def stop_test(self):
        self.is_running = False
        self.btn_start.config(text="START TEST", bg=BTN_START)
        self.status_label.config(text="STATUS: STOPPED", fg="#888888")


if __name__ == "__main__":
    root = tk.Tk()
    app = BotApp(root)
    root.mainloop()
