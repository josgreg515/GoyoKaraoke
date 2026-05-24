import streamlit as st
import whisper
import os

# Importamos moviepy de la forma más compatible posible
try:
    from moviepy.editor import ColorClip, CompositeVideoClip
    LIBRERIAS_OK = True
except Exception as e:
    LIBRERIAS_OK = False
    st.error(f"Error de librerías: {e}")

st.title("🎤 GoyoKaraoke")

if LIBRERIAS_OK:
    archivo = st.file_uploader("Sube tu canción", type=["mp3", "wav"])
    
    if archivo is not None:
        # Guardar audio de forma segura
        ruta_audio = "audio_temp.mp3"
        with open(ruta_audio, "wb") as f:
            f.write(archivo.getbuffer())
        
        if st.button("Generar Karaoke"):
            with st.spinner("Creando tu video..."):
                # 1. Transcripción simple
                model = whisper.load_model("base")
                resultado = model.transcribe(ruta_audio)
                
                # 2. Crear un video de prueba real (fondo negro)
                # Esto confirma que el motor de video funciona
                clip = ColorClip(size=(640, 360), color=(0,0,0), duration=5)
                archivo_video = "karaoke_final.mp4"
                clip.write_videofile(archivo_video, fps=24, logger=None)
                
                # 3. Mostrar el video
                if os.path.exists(archivo_video):
                    st.success("¡Video generado con éxito!")
                    st.video(archivo_video)
                    with open(archivo_video, "rb") as f:
                        st.download_button("Descargar Karaoke", f, "karaoke.mp4")
                else:
                    st.error("El video no se pudo crear.")
