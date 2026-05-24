import streamlit as st
import whisper
import os

st.title("🎤 GoyoKaraoke")

# ... (tu código de radio y uploader)

if audio_file is not None:
    # Guardar audio
    with open("temp_audio.mp3", "wb") as f:
        f.write(audio_file.getbuffer())
    
    if st.button("Generar Karaoke"):
        st.info("Transcribiendo con Whisper...")
        model = whisper.load_model("base")
        result = model.transcribe("temp_audio.mp3")
        st.write(result["text"])
