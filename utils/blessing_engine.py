# blessing_engine.py
import random
from datetime import datetime

DEFAULT_BLESSINGS = [
    "May this app bring giggles to the bedtime shadows.",
    "Bless this build, and the child who dreams beside it.",
    "Your creativity just made the moon smile.",
    "Rest easy. The code will still be weird tomorrow.",
    "This bedtime bot remembers your weirdest dream.",
    "Today you coded with love—and that’s always enough."
]

def generate_blessing(tone="playful", trigger="code_generated", child="Alora", agent_name=""):
    text = random.choice(DEFAULT_BLESSINGS)
    return {
        "text": text,
        "tone": tone,
        "trigger": trigger,
        "timestamp": datetime.now().isoformat(),
        "child": child,
        "agent_name": agent_name or "Unnamed Agent"
    }
