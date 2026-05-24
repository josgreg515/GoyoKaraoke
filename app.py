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

st.markdown("### El Creador de Karaokes para YouTube y TikTok")

# --- 3. CONFIGURACIÓN ---
formato = st.radio("Elige el formato:", ("YouTube (16:9)", "TikTok (9:16)"))
audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])

if "letra" not in st.session_state: st.session_state.letra = ""

if audio_file is not None:
    ruta_audio = os.path.abspath("temp_audio.mp3")
    with open(ruta_audio, "wb") as f: f.write(audio_file.getbuffer())

    # PASO 1: Transcripción con barra de progreso
    if st.button("👂 1. ANALIZAR LETRA"):
        with st.spinner("La IA está escuchando..."):
            model = whisper.load_model("base")
            result = model.transcribe(ruta_audio)
            st.session_state.letra = result["text"]
            st.success("¡Letra analizada!")

    # PASO 2: Revisión de Letra
    if st.session_state.letra:
        st.markdown("### ✍️ Corrige la letra (esto se mostrará en pantalla):")
        st.session_state.letra = st.text_area("Edita la letra aquí:", st.session_state.letra, height=150)

        # PASO 3: Generación de Video SIN ERRORES
        if st.button("🚀 2. GENERAR VIDEO BASE"):
            barra = st.progress(0)
            
            ancho, alto = (1280, 720) if formato == "YouTube (16:9)" else (720, 1280)
            
            # Fondo Azul (0, 0, 255)
            video_base = ColorClip(size=(ancho, alto), color=(0, 0, 255)).set_duration(10)
            barra.progress(50)
            
            # Logo arriba derecha
            if os.path.exists("logo.png"):
                logo = ImageClip("logo.png").resize(height=100).set_position(("right", "top")).set_duration(10)
                video_final = CompositeVideoClip([video_base, logo])
            else:
                video_final = video_base
            
            archivo_salida = "karaoke_goyo.mp4"
            video_final.write_videofile(archivo_salida, fps=24, codec="libx264", audio=ruta_audio)
            
            barra.progress(100)
            st.success("¡Tu video base está listo!")
            st.video(archivo_salida)
            
            with open(archivo_salida, "rb") as file:
                st.download_button("📥 DESCARGAR VIDEO BASE", data=file, 
                                   file_name="GoyoKaraoke_Base.mp4", mime="video/mp4")
            
            st.info("💡 Consejo: Usa tu editor de video favorito (CapCut/Premiere) para añadir la letra que acabas de corregir sobre este fondo azul.")
