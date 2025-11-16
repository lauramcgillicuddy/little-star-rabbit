"""
Text-to-Speech utilities for Little Star Rabbit
Provides reusable audio playback components
"""

import streamlit as st
from openai import OpenAI
from pathlib import Path
import tempfile
import base64

def get_tts_client():
    """Get OpenAI client for TTS"""
    from gpt_utils import get_openai_client
    return get_openai_client()

def text_to_speech(text: str) -> bytes:
    """Convert text to speech audio bytes"""
    client = get_tts_client()
    if not client:
        return None

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",  # Warm, friendly female voice
            input=text,
            speed=0.9  # Slightly slower for young children
        )
        return response.content
    except Exception as e:
        st.error("Couldn't create audio right now")
        return None

def render_read_aloud(text: str, label: str = "Read this aloud", unique_key: str = None):
    """
    Render text with a play/pause button for TTS

    Args:
        text: The text to display and read aloud
        label: Label for the play button
        unique_key: Unique key for the button (important for multiple instances)
    """
    # Display the text
    st.markdown(f"""
        <div style='
            background: rgba(255, 255, 255, 0.6);
            padding: 1.5rem;
            border-radius: 15px;
            border: 2px solid #ffb6d9;
            margin: 1rem 0;
        '>
            {text}
        </div>
    """, unsafe_allow_html=True)

    # Create unique key if not provided
    if not unique_key:
        import hashlib
        unique_key = hashlib.md5(text.encode()).hexdigest()[:8]

    # Play button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"🔊 {label}", key=f"tts_{unique_key}", use_container_width=True):
            with st.spinner("Creating audio..."):
                audio_bytes = text_to_speech(text)
                if audio_bytes:
                    # Create audio player
                    audio_base64 = base64.b64encode(audio_bytes).decode()
                    audio_html = f"""
                        <audio autoplay>
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
                    st.success("🎵 Playing!")

def render_read_aloud_simple(text: str, unique_key: str):
    """Simpler version that just shows a button"""
    if st.button(f"🔊 Read this aloud", key=f"tts_{unique_key}", use_container_width=True):
        with st.spinner("Creating audio..."):
            audio_bytes = text_to_speech(text)
            if audio_bytes:
                audio_base64 = base64.b64encode(audio_bytes).decode()
                audio_html = f"""
                    <audio autoplay>
                        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
