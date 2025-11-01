import json
import os

class VFSManager:
    def __init__(self, vfs_path=None):
        self.vfs_path = vfs_path
        self.fs = {"name": "/", "type": "dir", "children": []}
        self.current_path = [self.fs]

        if vfs_path and os.path.exists(vfs_path):
            try:
                with open(vfs_path, "r", encoding="utf-8") as f:
                    self.fs = json.load(f)
                self.current_path = [self.fs]
                print(f"[DEBUG] Loaded VFS from {vfs_path}")
            except Exception as e:
                print(f"[ERROR] Failed to load VFS: {e}")
        else:
            print("[INFO] Using empty in-memory VFS")

    def list_dir(self):
        """Возвращает список содержимого текущего каталога"""
        dir = self.current_path[-1]
        if "children" not in dir:
            return []
        return [child["name"] + ("/" if child["type"] == "dir" else "") for child in dir["children"]]

    def change_dir(self, name):
        """Переход в подкаталог"""
        if name == "..":
            if len(self.current_path) > 1:
                self.current_path.pop()
            return

        current_dir = self.current_path[-1]
        for child in current_dir.get("children", []):
            if child["type"] == "dir" and child["name"] == name:
                self.current_path.append(child)
                return
        raise ValueError(f"No such directory: {name}")

    def make_dir(self, name):
        """Создание нового каталога"""
        current_dir = self.current_path[-1]
        for child in current_dir.get("children", []):
            if child["name"] == name:
                raise ValueError("Directory already exists")

        new_dir = {"name": name, "type": "dir", "children": []}
        current_dir.setdefault("children", []).append(new_dir)

    def save(self, path=None):
        """Сохранение структуры в JSON"""
        target_path = path or self.vfs_path or "vfs_saved.json"
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(self.fs, f, indent=4, ensure_ascii=False)
            print(f"[INFO] VFS saved to {target_path}")
            return target_path
        except Exception as e:
            raise RuntimeError(f"Failed to save VFS: {e}")

    def get_current_path(self):
        """Возвращает строку текущего пути"""
        return "/" + "/".join(node["name"] for node in self.current_path[1:])
