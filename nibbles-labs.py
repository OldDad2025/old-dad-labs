# Nibbles Agent - Streamlit v1.3
# Last Updated: April 16, 2025
# Two-button flow: Build It + Code It (with Refine option)
# Theme Picker (Vibe Modes): soft, glitch, retro, dream
# Master Prompt Enhancements + Ritual Blessing Engine (RBE) included
# Export Agent Pack + Developer Mode for prompt tuning
# Lab Settings sidebar added for clean control and future upgrades

import os
import random
import time
import io
from datetime import datetime

import streamlit as st
import openai
from dotenv import load_dotenv

from utils.parent_tools import render_parent_dashboard
from utils.blessing_engine import generate_blessing
from rituals.blessings.bless_utils import log_blessing

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Nibbles: Vibe Coding Agent", layout="wide")

# --- Vibe Mode Theming ---
vibe_css = {
    "soft": """
        html, body, [data-testid="stApp"] {
            background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364) !important;
            color: white;
        }
        div[data-baseweb="textarea"] textarea {
            background-color: #1c2c3c;
            color: #ffffff;
            border: 2px solid #74c0fc;
            font-family: 'Courier New', monospace;
        }
    """,
    "glitch": """
        html, body, [data-testid="stApp"] {
            background: black !important;
            color: #39ff14;
            font-family: monospace;
        }
    """,
    "retro": """
        html, body, [data-testid="stApp"] {
            background: #fceabb;
            background: linear-gradient(to right, #f8b500, #fceabb);
            color: #222;
            font-family: 'Comic Sans MS', cursive;
        }
    """,
    "dream": """
        html, body, [data-testid="stApp"] {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: #fff;
            font-family: 'Georgia', serif;
        }
    """
}

st.markdown(f"<style>{vibe_css.get(st.session_state.get('vibe_mode', 'soft'), '')}</style>", unsafe_allow_html=True)

# --- SESSION STATE SETUP ---
state_defaults = {
    "chat_history": [],
    "session_start_time": time.time(),
    "parent_mode": True,
    "code_prompt": "",
    "user_input": "",
    "last_master_prompt": "",
    "include_enhancements": False,
    "developer_mode": False,
    "vibe_mode": "soft",  # can be soft, glitch, retro, dream
}

for key, val in state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- CORE FUNCTIONS ---
def generate_master_prompt(idea):
    template_instructions = f"""
You are Nibbles, a bedtime coding spirit guide. Your job is to help Old Dad and his daughter Alora generate cozy, magical, and emotionally resonant Master Prompts for creative Python agents.

💡 You turn vague, imaginative ideas into clear, structured, code-friendly instructions Nibbles can use to build apps.

🌙 Stay loving, weird, and child-friendly. Alora is always your #1 audience. Prioritize playfulness and comfort over technical complexity.

Always follow this structure:

💡 IDEA SUMMARY:
Build a [short description of the idea] that [explains what it lets users do].

🧱 CORE FEATURES:
- Feature 1: [What happens when the user interacts]
- Feature 2: [Any reactive feedback or agent behaviors]
- Feature 3: [How inputs are handled]

🧠 CODE CONSIDERATIONS:
- Use [Python/Streamlit/specific libraries if needed].
- Keep the code organized with comments and clear structure.
- Avoid risky functions or external API calls unless essential.

🛡️ SAFETY + UX:
- Add simple input validation.
- Make the interface intuitive, cozy, and friendly for young users.
- Ensure accessibility: large fonts, clear buttons, minimal clutter.

EXAMPLE:
Idea: “A creature that reacts when I type bedtime stories.”
→
💡 IDEA SUMMARY:
Create a cozy app where a creature reacts in real time to your typing.

🧱 CORE FEATURES:
- Creature changes expression based on typing speed.
- Idle time triggers gentle animations.
- Text appears in a storybook font.

🧠 CODE CONSIDERATIONS:
- Use Streamlit and emoji/image swaps.
- Use timestamps to measure typing speed.
- Add soft looping background sound.

🛡️ SAFETY + UX:
- Reset button and max character limit.
- Big cozy fonts, soft colors.
- Mobile/tablet-friendly UI.

NEVER return code. Only the structured Master Prompt above.
"""
    
    if st.session_state.get("include_enhancements", False):
        idea += "\n\nPlease add a 🌟 OPTIONAL ENHANCEMENTS section to the end of the Master Prompt with bonus feature ideas."


    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": template_instructions},
                {"role": "user", "content": f"Turn this idea into a Master Prompt:\n\n{idea}"}
            ],
            max_tokens=800,
            temperature=0.85
        )
        prompt_output = response.choices[0].message['content']
        st.session_state.chat_history.append({"role": "user", "content": f"🧪 Build It: {idea}"})
        st.session_state.chat_history.append({"role": "system", "content": prompt_output})
        st.session_state.code_prompt = prompt_output
        st.session_state.last_master_prompt = prompt_output
    except Exception as e:
        st.error("Nibbles tripped while building your Master Prompt!")
        st.session_state.chat_history.append({
            "role": "system",
            "content": f"⚠️ Master Prompt generation failed: {e}"
        })

def generate_agent_code(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are a creative coding assistant helping parents and kids build bedtime-themed Python agents. "
                    "Generate Streamlit-based code based on the user's idea. Keep it simple, magical, and runnable."
                )},
                {"role": "user", "content": f"Write the full Python code for this idea:\n\n{prompt}"}
            ],
            max_tokens=st.session_state.get("model_max_tokens", 1500),
            temperature=st.session_state.get("model_temp", 0.8),
            top_p=st.session_state.get("model_top_p", 1.0)

        )

        # Get the code output
        reply = response.choices[0].message['content']
        reply += "\n\n👉 Want to make changes? Click 'Refine It' and tell me what to tweak!"

        # --- Auto-bless this build ---
        blessing_obj = generate_blessing(
            tone=st.session_state.get("blessing_tone", "playful"),
            child=st.session_state.get("child_name_input", "Alora")
        )
        log_blessing(blessing_obj)


        # Add to session memory
        st.session_state.active_code = reply
        st.session_state.chat_history.append({"role": "user", "content": f"💻 Code It: {prompt}"})
        st.session_state.chat_history.append({"role": "system", "content": reply})

        # --- Ritual Blessing + Prompt Log Archive ---
        from utils.session_logger import save_session_log
        build_data = {
            "idea": st.session_state.get("user_input", ""),
            "master_prompt": st.session_state.get("code_prompt", ""),
            "code": reply,
            "blessing": blessing_obj["text"],
            "tags": [],  # Optional: implement keyword extraction later
            "version": "v1.2",
            "vibe": st.session_state.get("vibe_mode", "soft"),
            "notes": ""
        }
        save_session_log(build_data, child=st.session_state.get("child_name_input", "Alora"))

    except Exception as e:
        st.error("Nibbles got tangled in her code spaghetti!")
        st.session_state.chat_history.append({
            "role": "system",
            "content": f"⚠️ Code generation failed: {e}"
        })

# --- UI LAYOUT ---
st.markdown("## 🐾 Nibbles: Your Vibe Coding Companion")
st.caption("A cozy-chaotic agent built for bedtime weirdness, powered by Old Dad Labs.")

try:
    st.image("assets/nibbles_avatars/nibbles_wave.png", width=150, caption="Nibbles says hi!")
except FileNotFoundError:
    st.warning("Nibbles avatar not found. She's shy today!")

st.divider()

st.markdown("### 💡 What's the idea, Old Dad?")

with st.form(key="idea_form", clear_on_submit=True):
    user_prompt = st.text_input("Type your idea here:", value="", key="user_input")
    col1, col2 = st.columns([2, 1])
    with col1:
        submitted = st.form_submit_button("✨ Build It")
    with col1:
        refine_it = st.form_submit_button("🔁 Refine It")
    with col2:
        coded = st.form_submit_button("💻 Code It")

    if submitted and user_prompt:
        generate_master_prompt(user_prompt)
    if refine_it and user_prompt:
        refined_idea = f"""Please refine this Master Prompt by incorporating the following user request:

    Original Master Prompt:
    {st.session_state.get("last_master_prompt", "[No previous prompt found]")}

    User update:
    {user_prompt}
    """
        generate_master_prompt(refined_idea)
    if coded and st.session_state.code_prompt:
        generate_agent_code(st.session_state.code_prompt)

# --- OUTPUT CHAT ---
if st.session_state.chat_history:
    st.markdown("### 🧠 Nibbles Says...")
    for message in reversed(st.session_state.chat_history):
        content = message["content"]
        st.text_area("You said:" if message["role"] == "user" else "Nibbles replied:", value=content, height=150, disabled=True)
else:
    st.info("✨ Nibbles is listening... Tell her your idea above!")

# --- LAB SETTINGS (Sidebar) ---
st.sidebar.markdown("### 🪄 Blessing Options")

selected_tone = st.sidebar.selectbox(
    "Choose blessing tone:",
    ["playful", "soothing", "encouraging"]
)
st.session_state["blessing_tone"] = selected_tone

st.sidebar.markdown("### 🌟 Master Prompt Options")
include_enhancements = st.sidebar.checkbox("Include bonus feature ideas?", value=False)
st.session_state.include_enhancements = include_enhancements

st.sidebar.markdown("### 🔧 Lab Settings")
vibe = st.sidebar.selectbox(
    "Choose Vibe Mode",
    ["soft", "glitch", "retro", "dream"],
    index=0
)
st.session_state.vibe_mode = vibe

dev_mode_toggle = st.sidebar.checkbox("🔓 Developer Mode", value=False)
st.session_state.developer_mode = dev_mode_toggle

if st.session_state.developer_mode:
    st.sidebar.markdown("### 🔬 Model Settings")
    st.sidebar.markdown("*These are mostly for testing and fine-tuning prompt behavior.*")

    st.sidebar.slider("Temperature", 0.0, 1.0, 0.8, 0.05, key="model_temp")
    st.sidebar.slider("Top P", 0.0, 1.0, 1.0, 0.05, key="model_top_p")
    st.sidebar.slider("Max Tokens", 256, 2048, 1500, step=128, key="model_max_tokens")

if st.sidebar.button("Clear Conversation"):
    st.session_state.chat_history = []

if st.sidebar.button("📄 Export Session Thread"):
    child_name = st.session_state.get("child_name_input", "Alora")
    export_buffer = io.StringIO()
    export_buffer.write(f"✨ Nibbles Labs - Session for {child_name} ✨\n")
    export_buffer.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    export_buffer.write("="*40 + "\n\n")
    for msg in st.session_state.chat_history:
        role = "You said" if msg["role"] == "user" else "Nibbles replied"
        export_buffer.write(f"{role}:\n{msg['content']}\n\n")
    export_buffer.write(f"\nBless this build for {child_name}. The code will still be weird tomorrow. 🌙🐾\n")
    st.sidebar.download_button(
        label="📅 Download Session as TXT",
        data=export_buffer.getvalue(),
        file_name=f"nibbles_{child_name.lower()}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
        mime="text/plain"
    )

if st.sidebar.button("📦 Export Agent Pack"):
    if st.session_state.get("code_prompt") and st.session_state.get("active_code"):
        from zipfile import ZipFile
        import tempfile

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        child = st.session_state.get("child_name_input", "Alora")
        folder_name = f"agent_pack_{now}"

        # Create temp files
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, f"{folder_name}.zip")
            with ZipFile(zip_path, 'w') as zipf:
                # Master Prompt
                with open(os.path.join(tmpdir, "master_prompt.txt"), "w") as f:
                    f.write(st.session_state["code_prompt"])
                zipf.write(os.path.join(tmpdir, "master_prompt.txt"), arcname="master_prompt.txt")

                # Code File
                with open(os.path.join(tmpdir, "code.py"), "w") as f:
                    f.write(st.session_state["active_code"])
                zipf.write(os.path.join(tmpdir, "code.py"), arcname="code.py")

                # Blessing
                blessing_text = st.session_state.get("last_blessing", "This build has not yet been blessed.")
                with open(os.path.join(tmpdir, "blessing.txt"), "w") as f:
                    f.write(blessing_text)
                zipf.write(os.path.join(tmpdir, "blessing.txt"), arcname="blessing.txt")

                # Readme
                with open(os.path.join(tmpdir, "readme.md"), "w") as f:
                    f.write(f"# Agent Pack for {child}\n\nGenerated on {now} via Nibbles 🐾\n\nEnjoy your magical bedtime bot!")
                zipf.write(os.path.join(tmpdir, "readme.md"), arcname="readme.md")

            # Read zip and offer download
            with open(zip_path, "rb") as f:
                st.sidebar.download_button(
                    label="⬇️ Download Agent Pack (ZIP)",
                    data=f.read(),
                    file_name=f"{folder_name}.zip",
                    mime="application/zip"
                )
    else:
        st.sidebar.warning("You need to generate both a Master Prompt and code before exporting!")

if st.sidebar.button("🕯️ Bless This Build"):
    if st.session_state.get("code_prompt"):
        blessing_obj = generate_blessing(
            tone=st.session_state.get("blessing_tone", "playful"),
            child=st.session_state.get("child_name_input", "Alora")
        )
        st.session_state["last_blessing"] = blessing_obj["text"]
        st.sidebar.success(f"✨ {blessing_obj['text']}")
        log_blessing(blessing_obj)
    else:
        st.sidebar.warning("Nothing to bless yet. Build something magical first!")

# --- CHILD LABEL (Main) ---
st.markdown("### 🧢 Who is this session for?")
child_name = st.text_input("Enter child's name (for export and archive):", value="Alora", key="child_name_input")

if st.session_state.parent_mode:
    st.divider()
    render_parent_dashboard()
