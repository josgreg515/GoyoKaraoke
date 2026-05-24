import os
import subprocess
import sys

# Forzamos la instalación de la librería por si el servidor no la detectó
try:
    import moviepy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy", "imageio-ffmpeg"])

import streamlit as st
import whisper
from moviepy.editor import ColorClip, CompositeVideoClip

st.title("🎤 GoyoKaraoke - Modo Rescate")

archivo = st.file_uploader("Sube tu canción", type=["mp3", "wav"])

if archivo:
    if st.button("Generar Karaoke"):
        st.write("Procesando...")
        # Aquí continúa el código...
        st.success("¡Librerías cargadas!")
