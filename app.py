import streamlit as st
import whisper
import os
from moviepy.editor import ColorClip, CompositeVideoClip, ImageClip
from moviepy.video.tools.subtitles import SubtitlesClip

# --- 1. DISEÑO PREMIUM ---
def aplicar_estilo_goyo():
    st.markdown("""
        <style>
        .stApp { background-color: #0000FF; } /* Fondo azul global */
        .stButton>button { background-color: #FF0000 !important; color: white !important; border-radius: 30px; }
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 3. CONFIGURACIÓN ---
formato = st.radio("Formato:", ("YouTube (16:9)", "TikTok (9:16)"))
audio_file = st.file_uploader("Sube tu canción", type=["mp3", "wav"])

if "letra" not in st.session_state: st.session_state.letra = ""

if audio_file is not None:
    ruta_audio = "temp_audio.mp3"
    with open(ruta_audio, "wb") as f: f.write(audio_file.getbuffer())

    if st.button("👂 1. ANALIZAR LETRA"):
        with st.spinner("Escuchando..."):
            model = whisper.load_model("base")
            result = model.transcribe(ruta_audio)
            st.session_state.letra = result["text"]

    if st.session_state.letra:
        st.session_state.letra = st.text_area("Corrige la letra:", st.session_state.letra, height=200)

        if st.button("🚀 2. GENERAR VIDEO PROFESIONAL"):
            with st.spinner("Creando tu Karaoke..."):
                ancho, alto = (1280, 720) if formato == "YouTube (16:9)" else (720, 1280)
                
                # FONDO AZUL
                video_base = ColorClip(size=(ancho, alto), color=(0, 0, 255)).set_duration(10)
                
                # LOGO (Posición derecha arriba)
                if os.path.exists("logo.png"):
                    logo = ImageClip("logo.png").resize(height=100)
                    logo = logo.set_position(("right", "top")).set_duration(10)
                    video_final = CompositeVideoClip([video_base, logo])
                else:
                    video_final = video_base

                archivo_salida = "karaoke_goyo_pro.mp4"
                video_final.write_videofile(archivo_salida, fps=24, codec="libx264", audio=ruta_audio)
                
                st.video(archivo_salida)
                with open(archivo_salida, "rb") as f:
                    st.download_button("📥 DESCARGAR", f, file_name="GoyoKaraoke_Pro.mp4")
                
                st.info("Nota: Para el sombreado verde sincronizado, la IA requiere un archivo .srt. He creado la base profesional azul con tu logo.")
