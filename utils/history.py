import json
import os
HISTORY_FILE = "generated_history.json"
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []
def save_item(text):
    history = load_history()
    if text not in history:
        history.append(text)
    # Keep only the latest 100 items
    history = history[-100:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=2,
            ensure_ascii=False
        )
def get_recent_history(limit=20):
    history = load_history()
    return history[-limit:]