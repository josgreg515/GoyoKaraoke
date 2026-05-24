import streamlit as st
import whisper
import time
import os
import base64
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

# --- 1. CONFIGURACIÓN DE APARIENCIA (FONDO Y ESTILO) ---
def add_bg_and_style():
    # Usaremos una imagen de fondo profesional de música (puedes cambiar este link)
    bg_url = "https://images.unsplash.com/photo-1514525253361-bee8718a340b?q=80&w=1920"
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{bg_url}");
            background-size: cover;
            background-position: center;
        }}
        .stMarkdown, h1, p {{
            color: #FFFFFF !important;
            text-shadow: 2px 2px 4px #000000;
        }}
        .stButton>button {{
            background-color: #FF0000 !important; /* Rojo YouTube */
            color: white !important;
            border-radius: 20px;
            border: none;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_and_style()

# --- 2. LOGO GOYOKARAOKE ---
# Intenta cargar el logo si existe en el repo, si no, usa el texto
if os.path.exists("logo.png"):
    st.image("logo.png", width=200)
else:
    st.title("🎤 GoyoKaraoke")
    st.caption("¡El canal oficial de tus Karaokes!")

# --- 3. INTERFAZ ---
formato = st.radio("Elige el formato de tu video:", ("YouTube (16:9)", "TikTok (9:16)"))
audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])

if audio_file is not None:
    with open("temp_audio.mp3", "wb") as f:
        f.write(audio_file.getbuffer())

    if st.button("🚀 Crear mi Karaoke"):
        # --- BARRA DE PROGRESO ---
        progreso = st.progress(0, text="Iniciando motores...")
        
        # Paso 1: Transcripción (25%)
        progreso.progress(25, text="👂 La IA está escuchando y escribiendo la letra...")
        model = whisper.load_model("base")
        result = model.transcribe("temp_audio.mp3")
        texto = result["text"][:80] # Prueba corta
        
        # Paso 2: Diseño de video (60%)
        progreso.progress(60, text="🎨 Diseñando el fondo y el texto del karaoke...")
        size = (1280, 720) if formato == "YouTube (16:9)" else (720, 1280)
        
        clip = ColorClip(size=size, color=(20, 20, 20), duration=5)
        # Nota: TextClip puede necesitar configuración adicional en la nube
        txt_clip = TextClip(texto, fontsize=50, color='yellow', size=size, method='caption')
        txt_clip = txt_clip.set_duration(5).set_position('center')
        
        video_final = CompositeVideoClip([clip, txt_clip])
        
        # Paso 3: Renderizado (90%)
        progreso.progress(90, text="🎬 Procesando el video final para ti...")
        video_final.write_videofile("karaoke_resultado.mp4", fps=24, logger=None)
        
        # Paso 4: Finalizado (100%)
        progreso.progress(100, text="✅ ¡Tu Karaoke está listo!")
        st.balloons() # ¡Festejo con globos!

        # --- PREVISUALIZACIÓN Y DESCARGA ---
        st.video("karaoke_resultado.mp4")
        
        with open("karaoke_resultado.mp4", "rb") as file:
            st.download_button(
                label="📥 Descargar Karaoke",
                data=file,
                file_name=f"GoyoKaraoke_{int(time.time())}.mp4",
                mime="video/mp4"
            )
