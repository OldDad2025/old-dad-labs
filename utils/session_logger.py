import json
from datetime import datetime
import os

def save_session_log(data, child="Alora", folder="nibbles_logs"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(folder, f"build_{timestamp}.json")

    data["timestamp"] = timestamp
    data["child"] = child

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return file_path
