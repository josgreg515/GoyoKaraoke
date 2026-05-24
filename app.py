import streamlit as st
import os

# Configuración básica
st.set_page_config(page_title="GoyoKaraoke", page_icon="🎤")
st.title("🎤 GoyoKaraoke")

# Intentamos importar librerías complejas solo cuando sea necesario
try:
    import whisper
    from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
    LIBRERIAS_LISTAS = True
except ImportError as e:
    LIBRERIAS_LISTAS = False
    st.error(f"Error de carga de librerías: {e}. Revisa tu archivo requirements.txt")

if LIBRERIAS_LISTAS:
    audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])
    if audio_file:
        st.success("Archivo subido correctamente.")
        if st.button("Generar Karaoke"):
            st.info("Procesando...")
