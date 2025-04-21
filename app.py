import streamlit as st
import subprocess
import os
import signal
import pyttsx3


# TTS Setup
engine = pyttsx3.init()
engine.setProperty('rate', 160)

import threading

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()


# Streamlit Page Config
st.set_page_config(page_title="Assistive Vision App", layout="centered")
st.markdown("""
    <style>
    .title { font-size: 48px; font-weight: bold; text-align: center; color: #2c3e50; margin-bottom: 10px; }
    .subtitle { font-size: 20px; text-align: center; color: #7f8c8d; margin-bottom: 40px; }
    .stButton > button {
        width: 100%; height: 60px; font-size: 20px; font-weight: bold;
        border-radius: 10px; margin: 10px 0;
    }
    .object { background-color: #27ae60 !important; color: white !important; }
    .alert { background-color: #e67e22 !important; color: white !important; }
    .ocr { background-color: #2980b9 !important; color: white !important; }
    .scene { background-color: #8e44ad !important; color: white !important; }
    .stop { background-color: #c0392b !important; color: white !important; }
    .footer { font-size: 14px; text-align: center; margin-top: 60px; color: #999; }
    </style>
""", unsafe_allow_html=True)

# Title & Subtitle
st.markdown('<div class="title">👁️‍🗨️ Assistive Vision App</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">An integrated tool for object detection, text reading, and scene understanding.</div>', unsafe_allow_html=True)

# Initialize state
if "running_process" not in st.session_state:
    st.session_state.running_process = None
if "current_service" not in st.session_state:
    st.session_state.current_service = None
if "welcomed" not in st.session_state:
    speak("Welcome to the Assistive Vision App. Please select a service.")
    st.session_state.welcomed = True

# Services & scripts
services = {
    "🎯 Object Detection": ("obstacledetection-main.py", "object"),
    "📢 Obstacle Alert": ("obstacalert-main.py", "alert"),
    "📝 Text Recognition": ("text-to-speech-cam.py", "ocr"),
    "🖼️ Scene Description": ("posturedet-main.py", "scene")
}

# Button layout
cols = st.columns(2)
i = 0
for label, (script, css_class) in services.items():
    with cols[i % 2]:
        if st.button(label, key=label):
            # Stop current if any
            if st.session_state.running_process:
                st.warning(f"Stopping: {st.session_state.current_service}")
                try:
                    os.kill(st.session_state.running_process.pid, signal.SIGTERM)
                    st.success(f"Stopped: {st.session_state.current_service}")
                    speak(f"{st.session_state.current_service} stopped.")
                except Exception as e:
                    st.error(f"Error stopping previous service: {e}")
                    speak("Error stopping the previous service.")
                st.session_state.running_process = None
                st.session_state.current_service = None

            # Start new
            try:
                process = subprocess.Popen(["python", script])
                st.session_state.running_process = process
                st.session_state.current_service = label
                st.success(f"Started: {label}")
                speak(f"{label} started.")
            except Exception as e:
                st.error(f"Failed to start {label}: {e}")
                speak(f"Failed to start {label}")
    i += 1

# Stop Button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🛑 Stop Current Service", key="stop"):
    if st.session_state.running_process:
        try:
            os.kill(st.session_state.running_process.pid, signal.SIGTERM)
            st.success(f"Stopped: {st.session_state.current_service}")
            speak(f"{st.session_state.current_service} stopped.")
            st.session_state.running_process = None
            st.session_state.current_service = None
        except Exception as e:
            st.error(f"Error stopping service: {e}")
            speak("Error stopping the service.")
    else:
        st.warning("No service is currently running.")
        speak("No service is currently running.")

# Footer
st.markdown('<div class="footer">Made with ❤️ to assist the visually impaired</div>', unsafe_allow_html=True)
