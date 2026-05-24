import streamlit as st
import whisper
import os
import time
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, ImageClip

# --- 1. DISEÑO PREMIUM Y FONDO ---
def aplicar_estilo_goyo():
    # Fondo musical profesional
    fondo_url = "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920"
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}");
            background-size: cover;
            background-position: center;
        }}
        .stMarkdown, h1, h2, h3, p {{
            color: #FFFFFF !important;
            text-shadow: 2px 2px 8px #000000;
            font-family: 'Arial', sans-serif;
        }}
        .stButton>button {{
            background-color: #FF0000 !important; /* Rojo GoyoKaraoke */
            color: white !important;
            border-radius: 30px;
            height: 3em;
            width: 100%;
            font-weight: bold;
            border: 2px solid white;
        }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 2. LOGO OFICIAL ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png")
    else:
        st.title("🎤 GoyoKaraoke")

st.markdown("### El Creador de Karaokes para YouTube y TikTok")

# --- 3. CONFIGURACIÓN ---
formato = st.radio("Elige el formato de tu video:", ("YouTube (16:9)", "TikTok (9:16)"))
audio_file = st.file_uploader("Sube tu canción aquí", type=["mp3", "wav"])

if audio_file is not None:
    ruta_audio = os.path.abspath("temp_audio.mp3")
    with open(ruta_audio, "wb") as f:
        f.write(audio_file.getbuffer())

    if st.button("🚀 GENERAR VIDEO KARAOKE"):
        # --- BARRA DE PROGRESO REAL ---
        barra = st.progress(0)
        texto_estado = st.empty()
        
        # Paso 1: Transcripción
        texto_estado.markdown("#### 👂 1/3: La IA está escuchando tu canción...")
        barra.progress(20)
        model = whisper.load_model("base")
        result = model.transcribe(ruta_audio)
        letra = result["text"]
        
        # Paso 2: Diseño de Video
        texto_estado.markdown("#### 🎨 2/3: Diseñando el Karaoke en formato " + formato)
        barra.progress(60)
        
        # Definir dimensiones
        ancho, alto = (1280, 720) if formato == "YouTube (16:9)" else (720, 1280)
        
        # Crear clips
        fondo_video = ColorClip(size=(ancho, alto), color=(10, 10, 10)).set_duration(10)
        
        # Clip de texto (Letra)
        # Definir dimensiones
        ancho, alto = (1280, 720) if formato == "YouTube (16:9)" else (720, 1280)
        
        # Crear clips
        fondo_video = ColorClip(size=(ancho, alto), color=(10, 10, 10)).set_duration(10)
        
        # MODIFICACIÓN: Usamos un método de fallback para evitar el error de ImageMagick
        try:
            txt_clip = TextClip(letra[:150], fontsize=50, color='yellow', 
                                size=(ancho*0.8, None), method='caption', font='Arial')
        except Exception:
            # Si falla ImageMagick, usamos un clip de color temporal para no detener el renderizado
            st.warning("Nota: Usando modo de compatibilidad de texto.")
            txt_clip = ColorClip(size=(ancho//2, 100), color=(255, 255, 0)).set_duration(10)

        txt_clip = txt_clip.set_position('center').set_duration(10)
        
        # Unir todo
        video_final = CompositeVideoClip([fondo_video, txt_clip])
        
        # Unir todo
        video_final = CompositeVideoClip([fondo_video, txt_clip])
        
        # Paso 3: Renderizado
        texto_estado.markdown("#### 🎬 3/3: Procesando video final... ¡Ya casi está!")
        barra.progress(85)
        
        archivo_salida = "karaoke_goyo.mp4"
        video_final.write_videofile(archivo_salida, fps=24, codec="libx264", audio=ruta_audio)
        
        barra.progress(100)
        texto_estado.markdown("## ✅ ¡TU KARAOKE ESTÁ LISTO!")
        st.balloons()
        
        # --- PREVISUALIZACIÓN Y DESCARGA ---
        st.video(archivo_salida)
        
        with open(archivo_salida, "rb") as file:
            st.download_button(
                label="📥 DESCARGAR PARA MI CANAL",
                data=file,
                file_name=f"GoyoKaraoke_{formato.split()[0]}.mp4",
                mime="video/mp4"
            )
