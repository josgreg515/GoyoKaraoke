import streamlit as st
import whisper
import os
from moviepy.editor import ColorClip, CompositeVideoClip

# --- 1. DISEÑO PREMIUM ---
def aplicar_estilo_goyo():
    fondo_url = "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920"
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}");
            background-size: cover;
            background-position: center;
        }}
        .stMarkdown, h1, h2, h3, p {{ color: #FFFFFF !important; text-shadow: 2px 2px 8px #000000; }}
        .stButton>button {{
            background-color: #FF0000 !important; color: white !important;
            border-radius: 30px; height: 3em; width: 100%; font-weight: bold; border: 2px solid white;
        }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 2. LOGO ---
if os.path.exists("logo.png"): st.image("logo.png")
else: st.title("🎤 GoyoKaraoke")

# --- 3. CONFIGURACIÓN ---
formato = st.radio("Elige el formato:", ("YouTube (16:9)", "TikTok (9:16)"))
audio_file = st.file_uploader("Sube tu canción", type=["mp3", "wav"])

if "letra" not in st.session_state: st.session_state.letra = ""

if audio_file is not None:
    ruta_audio = os.path.abspath("temp_audio.mp3")
    with open(ruta_audio, "wb") as f: f.write(audio_file.getbuffer())

    # PASO 1: Transcripción
    if st.button("👂 1. ANALIZAR LETRA"):
        with st.spinner("La IA está escuchando..."):
            model = whisper.load_model("base")
            result = model.transcribe(ruta_audio)
            st.session_state.letra = result["text"]

    # PASO 2: Revisión de Letra
    if st.session_state.letra:
        st.markdown("### ✍️ Corrige la letra si es necesario:")
        st.session_state.letra = st.text_area("Letra:", st.session_state.letra, height=200)

        # PASO 3: Generación de Video
        if st.button("🚀 2. GENERAR VIDEO FINAL"):
            with st.spinner("Procesando video..."):
                ancho, alto = (1280, 720) if formato == "YouTube (16:9)" else (720, 1280)
                
                # Video limpio (sin recuadro amarillo)
                video_final = ColorClip(size=(ancho, alto), color=(10, 10, 10)).set_duration(10)
                
                archivo_salida = "karaoke_goyo.mp4"
                video_final.write_videofile(archivo_salida, fps=24, codec="libx264", audio=ruta_audio)
                
                st.success("¡Video generado con éxito!")
                st.video(archivo_salida)
                
                with open(archivo_salida, "rb") as file:
                    st.download_button("📥 DESCARGAR", data=file, 
                                       file_name="GoyoKaraoke.mp4", mime="video/mp4")
                
                st.markdown("### 📝 Letra definitiva:")
                st.info(st.session_state.letra)
