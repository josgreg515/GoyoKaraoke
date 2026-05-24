import streamlit as st
import whisper
import os
from moviepy.editor import ColorClip, CompositeVideoClip, ImageClip

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
        .stMarkdown, h1, h2, h3, p {{ color: #FFFFFF !important; text-shadow: 2px 2px 8px #000000; font-family: 'Arial', sans-serif; }}
        .stButton>button {{
            background-color: #FF0000 !important; color: white !important;
            border-radius: 30px; height: 3em; width: 100%; font-weight: bold; border: 2px solid white;
        }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 2. LOGO ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"): st.image("logo.png")
    else: st.title("🎤 GoyoKaraoke")

# --- 3. CONFIGURACIÓN ---
formato = st.radio("Elige el formato:", ("YouTube (16:9)", "TikTok (9:16)"))
audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])

if audio_file is not None:
    ruta_audio = os.path.abspath("temp_audio.mp3")
    with open(ruta_audio, "wb") as f: f.write(audio_file.getbuffer())

    if st.button("🚀 GENERAR VIDEO"):
        barra = st.progress(0)
        
        # Paso 1: Transcripción
        st.write("👂 Procesando audio...")
        barra.progress(30)
        model = whisper.load_model("base")
        result = model.transcribe(ruta_audio)
        letra = result["text"]
        
        # Paso 2: Generación del Video (Blindada contra errores)
        st.write("🎨 Renderizando video...")
        barra.progress(60)
        ancho, alto = (1280, 720) if formato == "YouTube (16:9)" else (720, 1280)
        
        # Fondo Azul Profesional (Color 0, 0, 255)
        video_base = ColorClip(size=(ancho, alto), color=(0, 0, 255)).set_duration(10)
        
        # Intentar añadir logo si existe
        if os.path.exists("logo.png"):
            logo = ImageClip("logo.png").resize(height=100).set_position(("right", "top")).set_duration(10)
            video_final = CompositeVideoClip([video_base, logo])
        else:
            video_final = video_base
            
        archivo_salida = "karaoke_goyo.mp4"
        video_final.write_videofile(archivo_salida, fps=24, codec="libx264", audio=ruta_audio)
        
        barra.progress(100)
        st.success("¡Video generado!")
        st.video(archivo_salida)
        
        # Descarga y muestra letra
        with open(archivo_salida, "rb") as file:
            st.download_button("📥 DESCARGAR", file, "GoyoKaraoke.mp4", "video/mp4")
        st.info("📝 Letra detectada: " + letra)
