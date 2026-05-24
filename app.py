import streamlit as st
import whisper
import os

st.title("🎤 GoyoKaraoke")

# Definimos la variable al principio
audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])

if audio_file is not None:
    st.write("Archivo detectado correctamente.")
    if st.button("Generar Karaoke"):
        st.write("Procesando...")
