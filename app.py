import streamlit as st
import whisper
import os

st.title("🎤 GoyoKaraoke")

formato = st.radio("Formato de salida:", ("YouTube (16:9)", "TikTok (9:16)"))
audio_file = st.file_uploader("Sube tu canción", type=["mp3", "wav"])

if audio_file is not None:
    with open("temp_audio.mp3", "wb") as f:
        f.write(audio_file.getbuffer())

    if st.button("Generar Karaoke"):
        st.info("La IA está trabajando...")
        
        # Simulamos la creación del archivo para que el código no falle
        # Más adelante pondremos aquí la lógica de moviepy real
        video_final = "karaoke_resultado.mp4"
        with open(video_final, "w") as f:
            f.write("test") 
            
        st.success("¡Video generado!")

        # Verificamos que el archivo existe antes de mostrarlo
        if os.path.exists(video_final):
            st.video(video_final)
            with open(video_final, "rb") as file:
                st.download_button("Descargar Video", file, file_name="karaoke.mp4")
