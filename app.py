import streamlit as st
import whisper
import os
import textwrap
from moviepy.editor import ColorClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont

# --- 1. DISEÑO PREMIUM ---
def aplicar_estilo_goyo():
    fondo_url = "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920"
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}"); background-size: cover; }}
        .stButton>button {{ background-color: #FF0000 !important; color: white !important; border-radius: 30px; height: 3em; }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 2. LOGO ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"): st.image("logo.png")
    else: st.title("🎤 GoyoKaraoke")

audio_file = st.file_uploader("Sube tu canción", type=["mp3", "wav"])
if "letra" not in st.session_state: st.session_state.letra = ""

if audio_file is not None:
    ruta_audio = "temp_audio.mp3"
    with open(ruta_audio, "wb") as f: f.write(audio_file.getbuffer())

    if st.button("👂 1. ANALIZAR LETRA"):
        with st.spinner("Escuchando..."):
            model = whisper.load_model("base")
            st.session_state.letra = model.transcribe(ruta_audio, language="es")["text"]

    if st.session_state.letra:
        st.markdown("### ✍️ Corrige la letra:")
        st.session_state.letra = st.text_area("Edita aquí:", st.session_state.letra, height=200)

        if st.button("🚀 2. GENERAR VIDEO FINAL"):
            barra = st.progress(0)
            
            # Crear fondo azul con letras dibujadas GRANDES
            ancho, alto = (1280, 720)
            img = Image.new('RGB', (ancho, alto), color=(0, 0, 255))
            d = ImageDraw.Draw(img)
            
            # --- NUEVA LÓGICA PARA BLOQUES DE TEXTO GRANDES ---
            import textwrap
            # Ajustamos el ancho (en número de caracteres por línea) a 30
            # Esto forzará bloques cortos de 3-4 líneas.
            lineas = textwrap.wrap(st.session_state.letra, width=30)
            
            y_pos = alto // 3 # Empezamos a escribir a 1/3 de la altura
            for linea in lineas:
                # Usamos una fuente más grande y legible
                # NOTA: Asegúrate de tener una fuente .ttf en tu carpeta si esta no carga.
                try:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
                except:
                    font = ImageFont.load_default()
                    st.warning("No se pudo cargar la fuente DejaVu, usando fuente básica. Las letras saldrán pequeñas.")
                d.text((100, y_pos), linea, fill=(255, 255, 255), font=font)
                y_pos += 70 # Espaciado entre líneas mayor para fuente grande
            # --- FIN DE LA LÓGICA ---
            
            img.save("frame.png")
            barra.progress(50)
            
            # Montar video
            video_base = ImageClip("frame.png").set_duration(10)
            if os.path.exists("logo.png"):
                logo = ImageClip("logo.png").resize(height=100).set_position(("right", "top")).set_duration(10)
                video_final = CompositeVideoClip([video_base, logo])
            else:
                video_final = video_base
            
            video_final.write_videofile("final.mp4", fps=24, codec="libx264", audio=ruta_audio)
            barra.progress(100)
            st.video("final.mp4")
            with open("final.mp4", "rb") as f: st.download_button("📥 DESCARGAR", f, "GoyoKaraoke.mp4")
