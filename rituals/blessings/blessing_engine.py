# blessing_engine.py
import os
from datetime import datetime
import streamlit as st

BLESSINGS_FOLDER = "rituals/blessings"
os.makedirs(BLESSINGS_FOLDER, exist_ok=True)

def generate_blessing():
    blessings = [
        "Rest easy. The code will still be weird tomorrow.",
        "Today you were small but strong. That matters.",
        "Your laughter echoed like magic in the lab.",
        "You were kind to yourself today. That's the real win."
    ]
    return st.selectbox("Choose a blessing to give:", blessings)

def save_blessing(blessing):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"blessing_{timestamp}.txt"
    with open(os.path.join(BLESSINGS_FOLDER, filename), "w") as f:
        f.write(blessing)
    st.success("Blessing saved to the Ritual Archive.")

def bless_this_build():
    st.subheader("🕊 Bless This Build")
    blessing = generate_blessing()
    if st.button("Bless it!"):
        save_blessing(blessing)

# This function would be called from the main app or other agents
# bless_this_build()