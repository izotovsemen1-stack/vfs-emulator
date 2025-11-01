from config import parse_arguments
from repl_gui import ShellGUI

def main():
    args = parse_arguments()
    app = ShellGUI(title="VFS Emulator")

    if args.script:
        app.append_output(f"[INFO] Running startup script: {args.script}")
        app.run_script(args.script)

    app.start()

if __name__ == "__main__":
    main()
