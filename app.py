import streamlit as st
import os
import yt_dlp

# --- 1. DISEÑO PREMIUM (Tu estilo original) ---
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

st.markdown("### Descarga videos de YouTube de forma rápida")

# --- 3. LÓGICA DE DESCARGA ---
url = st.text_input("Pega el enlace de YouTube aquí:")
formato = st.radio("¿Qué deseas descargar?", ("Video (MP4)", "Solo Audio (MP3)"))

if st.button("🚀 INICIAR DESCARGA"):
    if url:
        barra = st.progress(0)
        st.write("🔄 Conectando con YouTube...")
        
        # Configuración para yt-dlp
        opciones = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if formato == "Video (MP4)" else 'bestaudio/best',
            'outtmpl': 'descarga.%(ext)s',
        }
        
        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                st.write("⬇️ Descargando...")
                barra.progress(50)
                ydl.download([url])
                barra.progress(100)
            
            archivo = "descarga.mp4" if formato == "Video (MP4)" else "descarga.webm"
            
            st.success("¡Descarga completada!")
            with open(archivo, "rb") as f:
                st.download_button("📥 DESCARGAR ARCHIVO", f, file_name=f"GoyoDownload.{'mp4' if formato == 'Video (MP4)' else 'mp3'}")
        
        except Exception as e:
            st.error(f"Error al descargar: {e}")
    else:
        st.warning("Por favor, pega un enlace primero.")
