"""
VFS REPL prototype — Этап 1
Файл: vfs_repl.py

Реализовано:
1. GUI (tkinter) с заголовком окна "VFS"
2. Поле вывода (имитация терминала) и строка ввода
3. Парсер аргументов в кавычках (shlex)
4. Команды-заглушки: ls, cd, exit
5. Кнопка "Run demo" — демонстрация работы и обработки ошибок
"""

import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import shlex
import threading
import time
import sys

APP_TITLE = "VFS"


class VFSREPLApp:
    def __init__(self, master):
        self.master = master
        master.title(APP_TITLE)

        # Окно вывода (терминал)
        self.output = scrolledtext.ScrolledText(
            master, wrap=tk.WORD, height=20, width=80
        )
        self.output.pack(padx=8, pady=(8, 0), fill=tk.BOTH, expand=True)
        self.output.configure(state=tk.DISABLED)

        # Строка ввода
        frame = tk.Frame(master)
        frame.pack(fill=tk.X, padx=8, pady=8)
        self.prompt = tk.Label(frame, text="$ ")
        self.prompt.pack(side=tk.LEFT)
        self.entry = tk.Entry(frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.on_enter)

        # Кнопки управления
        btn_frame = tk.Frame(master)
        btn_frame.pack(fill=tk.X, padx=8, pady=(0, 8))
        run_demo_btn = tk.Button(btn_frame, text="Run demo", command=self.run_demo)
        run_demo_btn.pack(side=tk.LEFT)
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_output)
        clear_btn.pack(side=tk.LEFT, padx=(8, 0))

        # Словарь команд
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
        }

        self.cwd = "/"  # Текущий каталог (виртуальный)

        self.print_out("VFS REPL prototype started. Type commands or press 'Run demo'.\n")

    # -------------------------------------------------
    # Вспомогательные методы
    # -------------------------------------------------

    def clear_output(self):
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.configure(state=tk.DISABLED)

    def print_out(self, text):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    # -------------------------------------------------
    # Основная логика REPL
    # -------------------------------------------------

    def on_enter(self, event=None):
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        if not line.strip():
            return

        self.print_out(f"$ {line}\n")

        try:
            argv = shlex.split(line)
        except ValueError as e:
            self.print_out(f"Parse error: {e}\n")
            return

        cmd = argv[0]
        args = argv[1:]
        handler = self.commands.get(cmd)

        if handler:
            try:
                handler(args)
            except Exception as e:
                self.print_out(f"Error while running {cmd}: {e}\n")
        else:
            self.print_out(f"Unknown command: {cmd}\n")

    # -------------------------------------------------
    # Команды-заглушки
    # -------------------------------------------------

    def cmd_ls(self, args):
        self.print_out(f"ls called with args: {args}\n")

    def cmd_cd(self, args):
        self.print_out(f"cd called with args: {args}\n")
        if len(args) > 0:
            new = args[0]
            if new.startswith("/"):
                self.cwd = new
            else:
                if self.cwd.endswith("/"):
                    self.cwd = self.cwd + new
                else:
                    self.cwd = self.cwd + "/" + new
            self.print_out(f"cwd -> {self.cwd}\n")

    def cmd_exit(self, args):
        self.print_out("Exiting...\n")
        self.master.after(200, self.master.quit)

    # -------------------------------------------------
    # Демонстрация работы (этап 1)
    # -------------------------------------------------

    def run_demo(self):
        def demo_thread():
            demo_lines = [
                "ls",
                "ls -l /home",
                "cd /",
                "cd \"my folder\"",
                "cd \"incomplete quote",  # ошибка парсинга
                "unknowncmd arg1",
                "exit",
            ]
            for line in demo_lines:
                time.sleep(0.6)
                self.entry.delete(0, tk.END)
                self.entry.insert(0, line)
                self.master.event_generate("<<DemoEnter>>")

        def on_demo_enter(event=None):
            self.on_enter()

        self.master.bind("<<DemoEnter>>", on_demo_enter)
        t = threading.Thread(target=demo_thread, daemon=True)
        t.start()


# -------------------------------------------------
# Точка входа
# -------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Запуск GUI: python vfs_repl.py")
        print("Опции: --demo — запускает демонстрацию команд в GUI")
        sys.exit(0)

    root = tk.Tk()
    app = VFSREPLApp(root)
    root.mainloop()
