import streamlit as st
import whisper
import os
from moviepy.editor import ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont

# --- 1. DISEÑO PREMIUM ---
def aplicar_estilo_goyo():
    fondo_url = "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920"
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}"); background-size: cover; }}
        .stButton>button {{ background-color: #FF0000 !important; color: white !important; border-radius: 30px; }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 2. LOGO ---
if os.path.exists("logo.png"): st.image("logo.png")
else: st.title("🎤 GoyoKaraoke")

audio_file = st.file_uploader("Sube tu canción", type=["mp3", "wav"])
if "letra" not in st.session_state: st.session_state.letra = ""

if audio_file is not None:
    ruta_audio = "temp_audio.mp3"
    with open(ruta_audio, "wb") as f: f.write(audio_file.getbuffer())

    # PASO 1: Transcripción (Forzando español)
    if st.button("👂 1. ANALIZAR LETRA"):
        with st.spinner("Escuchando..."):
            model = whisper.load_model("base")
            result = model.transcribe(ruta_audio, language="es")
            st.session_state.letra = result["text"]

    # PASO 2: Edición (Restaurada)
    if st.session_state.letra:
        st.markdown("### ✍️ Corrige la letra:")
        st.session_state.letra = st.text_area("Edita aquí:", st.session_state.letra, height=200)

        # PASO 3: Generación
        if st.button("🚀 2. GENERAR VIDEO FINAL"):
            barra = st.progress(0)
            
            # Crear fondo azul
            img = Image.new('RGB', (1280, 720), color=(0, 0, 255))
            d = ImageDraw.Draw(img)
            d.text((50, 300), st.session_state.letra[:200], fill=(255, 255, 255))
            img.save("frame.png")
            
            video_base = ImageClip("frame.png").set_duration(10)
            
            # Añadir logo
            if os.path.exists("logo.png"):
                logo = ImageClip("logo.png").resize(height=100).set_position(("right", "top")).set_duration(10)
                video_final = CompositeVideoClip([video_base, logo])
            else:
                video_final = video_base
            
            video_final.write_videofile("final.mp4", fps=24, codec="libx264", audio=ruta_audio)
            barra.progress(100)
            st.video("final.mp4")
            with open("final.mp4", "rb") as f: st.download_button("📥 DESCARGAR", f, "GoyoKaraoke.mp4")
