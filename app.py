import streamlit as st

st.title("🎤 GoyoKaraoke")

# 1. Selección de formato
formato = st.radio("Elige el formato de tu video:", ("YouTube (Horizontal - 16:9)", "TikTok (Vertical - 9:16)"))

# 2. Carga de archivo
audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])

if audio_file is not None:
    st.write(f"Has seleccionado formato: {formato}")
    
    if st.button("Generar Karaoke"):
        st.info("Procesando la música y sincronizando la letra...")
        
        # Aquí es donde, más adelante, conectaremos Whisper y MoviePy
        # para recortar y exportar el video según el formato elegido.
        
        st.success("¡Tu karaoke está listo!")
        st.download_button("Descargar Video", data=b"video_data", file_name="karaoke_goyo.mp4")
