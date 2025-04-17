import os
import json

def log_blessing(blessing, folder="rituals/blessings"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, "bless_log.json1")
    with open(filepath, "a") as f:
        f.write(json.dumps(blessing) + "\n")
