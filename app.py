import streamlit as st
import whisper
import os

st.title("🎤 GoyoKaraoke")

audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])

if audio_file is not None:
    st.write("Archivo detectado. Preparando procesamiento...")
    
    with open("temp_audio.mp3", "wb") as f:
        f.write(audio_file.getbuffer())
        
    if st.button("Generar Karaoke"):
        st.info("La IA está trabajando...")
        model = whisper.load_model("base")
        result = model.transcribe("temp_audio.mp3")
        st.success("¡Transcripción lista!")
        st.text_area("Letra detectada:", result["text"])
