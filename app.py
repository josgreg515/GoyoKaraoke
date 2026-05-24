import streamlit as st
import os
from pytube import YouTube

# --- 1. DISEÑO PREMIUM ---
def aplicar_estilo_goyo():
    fondo_url = "https://images.unsplash.com/photo-1493225255756-d9584f8606e9?q=80&w=1920"
    st.markdown(f"""
        <style>
        .stApp {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}"); background-size: cover; }}
        .stButton>button {{ background-color: #FF0000 !important; color: white !important; border-radius: 30px; height: 3em; }}
        h1, h2, h3, p {{ color: white !important; }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_goyo()

# --- 2. LOGO ---
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if os.path.exists("logo.png"): st.image("logo.png")
    else: st.title("📥 GoyoDownloader")

# --- 3. LÓGICA DE DESCARGA ---
url = st.text_input("Pega el enlace de YouTube aquí:")

if url:
    try:
        # Visualización previa
        st.video(url)
        
        formato = st.radio("¿Qué deseas descargar?", ("Video (MP4)", "Solo Audio (MP3)"))
        
        if st.button("🚀 INICIAR DESCARGA"):
            barra = st.progress(0)
            
            yt = YouTube(url)
            barra.progress(30)
            
            if formato == "Video (MP4)":
                # Filtramos por streams que tengan video y audio
                stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            else:
                stream = yt.streams.filter(only_audio=True).first()
                
            stream.download(filename="descarga_goyo")
            barra.progress(100)
            st.success("¡Descarga lista!")
            
            with open("descarga_goyo", "rb") as f:
                st.download_button("📥 DESCARGAR ARCHIVO", f, file_name="GoyoDescarga.mp4")
                
    except Exception as e:
        st.error("No se pudo cargar el video. Revisa el enlace o intenta de nuevo.")
