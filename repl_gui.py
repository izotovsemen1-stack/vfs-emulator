import tkinter as tk
from tkinter import scrolledtext, messagebox
import shlex
from vfs.vfs_manager import VFSManager

class ShellGUI:
    def __init__(self, title="VFS Emulator", vfs_path=None):
        self.vfs = VFSManager(vfs_path)
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("700x400")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.text_area.pack(expand=True, fill='both')

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill='x')
        self.entry.bind("<Return>", self.process_command)

        self.append_output("Welcome to VFS Emulator!\nType 'help' or 'exit' to quit.\n")

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
                self.append_output("\n".join(items) if items else "(empty)")

            elif cmd == "cd":
                if not args:
                    raise ValueError("Usage: cd <directory>")
                self.vfs.change_dir(args[0])
                self.append_output(f"Changed directory to {self.vfs.get_current_path()}")

            elif cmd == "mkdir":
                if not args:
                    raise ValueError("Usage: mkdir <name>")
                self.vfs.make_dir(args[0])
                self.append_output(f"Created directory: {args[0]}")

            elif cmd == "vfs-save":
                path = args[0] if args else None
                saved_to = self.vfs.save(path)
                self.append_output(f"VFS saved to {saved_to}")

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
