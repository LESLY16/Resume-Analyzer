import json
import os
from threading import Lock

COUNTER_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "visitor_count.json")
_lock = Lock()

def _init_file():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            json.dump({"count": 0}, f)

def get_count() -> int:
    _init_file()
    with open(COUNTER_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return int(data.get("count", 0))

def increment_count() -> int:
    _init_file()
    with _lock:
        with open(COUNTER_FILE, encoding="utf-8") as f:
            data = json.load(f)
        data["count"] = int(data.get("count", 0)) + 1
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    return data["count"]
