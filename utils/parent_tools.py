# utils/parent_tools.py

import streamlit as st

def render_parent_dashboard():
    """
    This function renders the Parent Mode dashboard—
    a space for moms, dads, and future Old Dads to prepare tools,
    leave blessings, and build memory machines.
    """

    st.markdown("### 🧸 Parent Mode: Prepping for Baby Magic")
    st.write("Tools, messages, and prep rituals for 0–9 month vibes.")

    # -- Blessing Builder --
    with st.expander("✝️ Build a Blessing"):
        blessing = st.text_area("Write a short blessing or message:")
        if st.button("Save Blessing"):
            st.session_state.last_blessing = blessing
            st.success("Blessing saved! Nibbles is wagging her tail.")

    # -- Agent Prep --
    with st.expander("🤖 Prepare a Custom Agent"):
        agent_name = st.text_input("Name your agent")
        agent_purpose = st.text_area("What does this agent do?")
        if st.button("Save Agent Draft"):
            # This will evolve later, but for now:
            st.write(f"Agent '{agent_name}' saved with purpose: {agent_purpose}")

    # -- Audio/Memory Notes (Future Feature) --
    with st.expander("🎙️ Leave a Voice Note (Coming Soon)"):
        st.write("You'll be able to record bedtime messages for later here.")

    # -- Mode Toggles --
    st.markdown("### 🔧 Settings")
    st.checkbox("Enable Nurture Mode", key="nurture_mode")
    st.checkbox("Enable Legacy Mode", key="legacy_mode")
