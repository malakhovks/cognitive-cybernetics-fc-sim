import os, json, yaml
def ensure_dir(p: str) -> None: os.makedirs(p, exist_ok=True)
def load_yaml(path: str):
    with open(path, "r") as f: return yaml.safe_load(f)
def write_json(path: str, obj) -> None:
    with open(path, "w") as f: json.dump(obj, f, indent=2)
