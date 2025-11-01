import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="VFS Emulator Configuration")
    parser.add_argument("--vfs", type=str, help="Path to VFS JSON file", default=None)
    parser.add_argument("--script", type=str, help="Path to startup script", default=None)
    args = parser.parse_args()

    print("[DEBUG] Loaded configuration:")
    print(f"  VFS path: {args.vfs if args.vfs else 'None (default in-memory VFS)'}")
    print(f"  Startup script: {args.script if args.script else 'None'}")

    return args
