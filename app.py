import streamlit as st
import whisper
import os
import time
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

st.title("🎤 GoyoKaraoke")

# --- INTERFAZ ---
formato = st.radio("Formato de salida:", ("YouTube (16:9)", "TikTok (9:16)"))
audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])

if audio_file is not None:
    # Ruta absoluta para evitar errores de lectura
    ruta_audio = os.path.abspath("temp_audio.mp3")
    with open(ruta_audio, "wb") as f:
        f.write(audio_file.getbuffer())

    if st.button("🚀 Crear mi Karaoke"):
        if os.path.exists(ruta_audio):
            progreso = st.progress(0, text="Iniciando...")
            
            # Transcripción
            progreso.progress(30, text="👂 La IA está escuchando...")
            model = whisper.load_model("base")
            result = model.transcribe(ruta_audio)
            texto = result["text"][:100]
            
            # Generar video
            progreso.progress(70, text="🎬 Generando video...")
            size = (1280, 720) if formato == "YouTube (16:9)" else (720, 1280)
            
            clip = ColorClip(size=size, color=(20, 20, 20), duration=5)
            txt_clip = TextClip(texto, fontsize=50, color='yellow', size=size, method='caption')
            txt_clip = txt_clip.set_duration(5).set_position('center')
            
            video = CompositeVideoClip([clip, txt_clip])
            video.write_videofile("karaoke_final.mp4", fps=24, logger=None)
            
            progreso.progress(100, text="✅ ¡Listo!")
            st.video("karaoke_final.mp4")
            
            with open("karaoke_final.mp4", "rb") as file:
                st.download_button("📥 Descargar Karaoke", file, file_name="karaoke.mp4")
        else:
            st.error("Error: El archivo de audio no se guardó correctamente.")
