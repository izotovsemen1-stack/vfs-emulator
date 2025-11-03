import tkinter as tk
from tkinter import scrolledtext, messagebox
import shlex
import time
from vfs.vfs_manager import VFSManager

class ShellGUI:
    def __init__(self, title="VFS Emulator", vfs_path=None):
        self.vfs = VFSManager(vfs_path)
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("700x400")

        self.start_time = time.time()
        self.username = "user"

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.text_area.pack(expand=True, fill='both')

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill='x')
        self.entry.bind("<Return>", self.process_command)

        self.append_output("Welcome to VFS Emulator!")
        self.append_output("Type 'help' or 'exit' to quit.\n")

    def append_output(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    def process_command(self, event=None, command=None):
        cmd_input = command if command else self.entry.get().strip()
        if not cmd_input:
            return
        self.append_output(f"> {cmd_input}")
        self.entry.delete(0, tk.END)

        try:
            parts = self._parse_command(cmd_input)
            cmd = parts[0]
            args = parts[1:]

            if cmd == "exit":
                self.append_output("Exiting...")
                self.root.quit()

            elif cmd == "ls":
                items = self.vfs.list_dir()
                self.append_output("(empty)" if not items else "  ".join(items))

            elif cmd == "cd":
                if not args:
                    raise ValueError("Usage: cd <directory>")
                self.vfs.change_dir(args[0])
                self.append_output(f"Changed directory to {self.vfs.get_current_path()}")

            elif cmd == "mkdir":
                if not args:
                    raise ValueError("Usage: mkdir <directory>")
                self.vfs.make_dir(args[0])
                self.append_output(f"Created directory: {args[0]}")

            elif cmd == "rmdir":
                if not args:
                    raise ValueError("Usage: rmdir <directory>")
                self.vfs.remove_dir(args[0])
                self.append_output(f"Removed directory: {args[0]}")

            elif cmd == "pwd":
                self.append_output(self.vfs.get_current_path())

            elif cmd == "whoami":
                self.append_output(self.username)

            elif cmd == "uptime":
                elapsed = time.time() - self.start_time
                minutes, seconds = divmod(int(elapsed), 60)
                self.append_output(f"Uptime: {minutes}m {seconds}s")

            elif cmd == "vfs-save":
                path = args[0] if args else None
                saved_to = self.vfs.save(path)
                self.append_output(f"VFS saved to {saved_to}")

            elif cmd == "help":
                self.append_output(
                    "Available commands:\n"
                    "  ls          - list directory contents\n"
                    "  cd <dir>    - change directory\n"
                    "  mkdir <n>   - create directory\n"
                    "  rmdir <n>   - remove empty directory\n"
                    "  pwd         - print working directory\n"
                    "  whoami      - show current user\n"
                    "  uptime      - show time since start\n"
                    "  vfs-save [p]- save current VFS\n"
                    "  exit        - quit emulator"
                )

            else:
                self.append_output(f"Unknown command: {cmd}")

        except Exception as e:
            self.append_output(f"Error: {e}")

    def _parse_command(self, command_str):
        return shlex.split(command_str)

    def run_script(self, script_path):
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    self.process_command(command=line)
        except Exception as e:
            messagebox.showerror("Script Error", f"Script execution stopped: {e}")
            self.append_output(f"[ERROR] Script stopped: {e}")

    def start(self):
        self.root.mainloop()
